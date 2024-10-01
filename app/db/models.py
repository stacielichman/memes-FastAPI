from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base


class Meme(Base):
    """
    Database model representing a meme.
    """
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String)
