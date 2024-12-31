"""main.py

This module is entry point into fast api application

"""

from fastapi import FastAPI,status,Depends,HTTPException
from sqlalchemy.orm import Session
from models import MovieRequestModel,MovieResponseModel 
from db.database import Base, SessionLocal, engine
from db.schema import Movies


Base.metadata.create_all(bind=engine)


# Get database
def get_db():
    """
    This method gets the database connection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app = FastAPI(
    title="movies database",
    summary="movie database for learning Fast API",
    version="1.0.0",
)


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: MovieRequestModel, db: Session = Depends(get_db)
) -> MovieResponseModel:
    """
    Create a new movie record in the database.

    Args:
        movie (MovieRequestModel): Details of the movie to be created.

    Returns:
        MovieResponseModel: Details of the newly created movie, including its assigned `id`.
    
    
    """
    db_movie = Movies(
        title=movie.title,
        rating=movie.rating,
        director=movie.director,
        actor=movie.actor,
        actress=movie.actress,
        producer=movie.producer
    )
    
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return MovieResponseModel(
        id=db_movie.id,
        title=movie.title,
        rating=movie.rating,
        director=movie.director,
        actor=movie.actor,
        actress=movie.actress,
        producer=movie.producer
    )




@app.delete("/movies/{id}",response_model=MovieResponseModel)
def delete_movie(id: int, db: Session = Depends(get_db)) -> MovieResponseModel:
    """This method deletes a movie based on its id
    Args:
        id (int): Movie id
        
    Raises:
        HTTPException: Not Found
    Returns:
        detetes the mobie accordung to its id
    """
    # Fetch the movie from the database
    movie = db.query(Movies).filter(Movies.id == id).first()

    # If the movie doesn't exist, raise a 404 error
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    # Delete the movie from the database
    db.delete(movie)
    db.commit()

    # Return a success message
    return {"detail": "Movie deleted"}


@app.get("/movies/{title}",response_model=MovieResponseModel)
def get_movie(title:str, db: Session = Depends(get_db)) -> MovieResponseModel:
    """This method returns the product by id
    Args:
        title (str): title of the movie
        
    Raises:
        HTTPException: raises 404 error
    Returns:
    MovieResponseModel: details of the movie
    """
    movie = db.query(Movies).filter(Movies.title == title).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieResponseModel(
        id=movie.id,
        title=movie.title,
        rating=movie.rating,
        director=movie.director,
        actor=movie.actor,
        actress=movie.actress,
        producer=movie.producer
    )

@app.put("/movies/{id}", response_model=MovieResponseModel)
def update_movie(id:int, movie: MovieRequestModel, db: Session = Depends(get_db)) -> MovieResponseModel:
    """
    This endpoint updates an existing movie record in the database.

    Args:
        id (int): The ID of the movie to update.
        movie (MovieRequestModel): The new details for the movie.
        

    Raises:
        HTTPException: If the movie is not found or if there is an issue with database interaction.

    Returns:
        MovieResponseModel: Details of the updated movie.
    """
    # Fetch the movie from the database
    db_movie = db.query(Movies).filter(Movies.id == id).first()

    # If the movie doesn't exist, raise a 404 error
    if db_movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    # Update fields with new values from the request
    db_movie.title = movie.title
    db_movie.rating = movie.rating
    db_movie.director = movie.director
    db_movie.actor = movie.actor
    db_movie.actress = movie.actress
    db_movie.producer = movie.producer

    # Commit changes to the database
    db.commit()
    db.refresh(db_movie)

    # Return updated movie details
    return MovieResponseModel(
        id=db_movie.id,
        title=db_movie.title,
        rating=db_movie.rating,
        director=db_movie.director,
        actor=db_movie.actor,
        actress=db_movie.actress,
        producer=db_movie.producer
    )
