import json
from typing import Optional

from pydantic import BaseModel, model_validator


class MemeBase(BaseModel):
    """
    Base schema for pydantic meme objects.
    """
    title: str
    description: Optional[str] = None


class MemeIn(MemeBase):
    """
    Schema for creating a new meme.
    Validates if the input is a JSON string and converts it to a dictionary.
    """

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class MemeOut(MemeBase):
    """
    Schema for returning a meme object to user.
    """
    title: str
    description: Optional[str] = None
    image_url: str

    class Config:
        from_attributes = True


class MemeUpdate(BaseModel):
    """
    Schema for updating an existing meme.
    """
    title: Optional[str] = None
    description: Optional[str] = None
