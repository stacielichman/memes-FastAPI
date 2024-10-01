from sqlalchemy.future import select
from typing import List, Optional

from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.models import Meme
from app.db.schemas import MemeIn, MemeUpdate


async def get_memes_db(session: Session, offset: int, limit: int) -> List[Meme]:
    """
    Gets a list of memes from the database.

    Args:
        offset: Number of skipped memes
        limit: Number of memes per page
        session: Database session

    Returns:
        A list of memes
    """
    memes = await session.execute(select(models.Meme).offset(offset).limit(limit))
    return memes.scalars().all()


async def get_meme_db(session: Session, meme_id: int) -> Meme:
    """
    Get a meme from the database by its id.

    Args:
        meme_id (int): The id of the meme to get
        session: Database session

    Returns:
        object: The meme object
    """
    meme = await session.execute(select(Meme).filter(Meme.id == meme_id))
    return meme.scalars().first()


async def upload_meme_db(session: Session, meme: MemeIn, file_url: str) -> Meme:
    """
    Uploads a new meme into the database.

    Args:
        session: The database session
        meme: Input data of the meme
        file_url: The URL of the uploaded meme

    Returns:
        The created meme object
    """
    db_meme = Meme(**meme.dict(), image_url=file_url)
    session.add(db_meme)
    await session.commit()
    return db_meme


async def update_meme_db(session: Session, meme_id: int, meme_update: MemeUpdate):
    """
    Updates a meme in the database.

    Args:
        session: The database session
        meme_id: The id of the meme to update
        meme_update: The meme data to update

    Returns:
        The updated meme object if found, otherwise None
    """
    db_meme = await get_meme_db(session, meme_id)
    if db_meme:
        for field, value in meme_update.dict(exclude_none=True).items():
            setattr(db_meme, field, value)
        session.commit()
        return db_meme


async def delete_meme_db(session: Session, meme_id: int) -> Optional[Meme]:
    """
    Deletes a meme from the database.

    Args:
        session: The database session
        meme_id: The id of the meme to delete

    Returns:
        The deleted meme object if found, otherwise None.
    """
    result = await session.execute(select(Meme).filter(Meme.id == meme_id))
    db_meme = result.scalars().first()
    if db_meme:
        await session.delete(db_meme)
        await session.commit()
    return db_meme
