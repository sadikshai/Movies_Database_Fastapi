"""
models.py

this modeule contains the desighn for request and response model

"""

from pydantic import BaseModel,Field


class MovieRequestModel(BaseModel):
    """
    This model represents the request for Movie
    """

    title:str=Field(title="title of the movie ")
    rating:str=Field(title="rating of the movie")
    director:str=Field(title="director of the movie")
    actor:str=Field(title="name of the actor")
    actress:str=Field(title="actress of the movie")
    producer:str=Field(title="producer of the movie")



class MovieResponseModel(BaseModel):
    """
    This model represents the response for Movie
    """

    id: int
    title: str
    rating: str
    director: str
    actor: str
    actress: str
    producer: str
