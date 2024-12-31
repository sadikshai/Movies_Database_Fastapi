from sqlalchemy import Column, Integer, String
from db.database import Base  

class Movies(Base):
    """This model represents the table in the database"""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))  
    rating = Column(String(100))
    director = Column(String(100))
    actor = Column(String(100))
    actress = Column(String(100))
    producer = Column(String(100))



