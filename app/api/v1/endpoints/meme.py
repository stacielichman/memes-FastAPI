from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core import config
from app.crud.crud import get_meme_db, get_memes_db, upload_meme_db, update_meme_db, delete_meme_db
from app.db.models import Meme
from app.dependencies import get_db
from app.minio import upload_file_to_minio
from app.db.schemas import MemeOut, MemeIn, MemeUpdate


router = APIRouter()


@router.get("/memes/", response_model=List[MemeOut])
async def get_memes(
        offset: int = 0,
        limit: int = 10,
        session: Session = Depends(get_db)) -> List[Meme]:
    """
    Gets a list of memes.

    Args:
        offset: Number of skipped memes
        limit: Number of memes per page
        session: Database session

    Returns:
        list: A list of memes
    """
    memes = await get_memes_db(session, offset=offset, limit=limit)
    return memes


@router.get("/memes/{meme_id}", response_model=MemeOut)
async def get_meme(meme_id: int, session: Session = Depends(get_db)) -> Meme:
    """
    Gets a meme by its id.

    Args:
        meme_id (int): The id of the meme to get
        session: Database session

    Returns:
        object: The meme object

    Raises:
        HTTPException: If the meme is not found
    """

    meme = await get_meme_db(session, meme_id)
    if meme is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return meme


@router.post("/memes/", response_model=MemeOut)
async def post_meme(meme: MemeIn, file: UploadFile, session: Session = Depends(get_db)) -> Optional[Meme]:
    """
    Posts a new meme.

    Args:
        meme: Input model of the meme
        file: Image file
        session: Database session

    Returns:
        The created meme object

    Raises:
        HTTPException: If a file is not uploaded,
                       if the file is not an image,
                       if the file exceeds size limit,
                       if there is an error uploading the file to S3 storage
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if file.content_type not in config.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image type. The allowed image types are {', '.join(config.ALLOWED_IMAGE_TYPES)}"
        )
    if file.size > config.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the maximum limit of {config.MAX_FILE_SIZE // (1024 * 1024)} MB"
        )
    try:
        file_url = upload_file_to_minio(file)
        print(file)
        return await upload_meme_db(session, meme, str(file_url))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/memes/{meme_id}", response_model=MemeOut)
async def update_meme(meme_id: int, meme_update: MemeUpdate, session: Session = Depends(get_db)) -> Optional[Meme]:
    """
    Updates an existing meme.

    Args:
        meme_id (int): ID of the meme to update
        meme_update: Meme data to update
        session: Database session

    Returns:
        Updated meme object

    Raises:
        HTTPException: If the meme is not found
    """
    db_meme = await update_meme_db(session, meme_id, meme_update)
    if db_meme is None:
        raise HTTPException(status_code=404, detail=f"Meme with id {meme_id} is not found")
    return db_meme


@router.delete("/memes/{meme_id}", response_model=MemeOut)
async def delete_meme(meme_id: int, session: Session = Depends(get_db)):
    """
    Deletes a meme.

    Args:
        meme_id (int): The id of the meme to delete
        session: Database session

    Returns:
        Deleted meme object

    Raises:
        HTTPException: If the meme is not found
    """
    db_meme = await delete_meme_db(session, meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail=f"Meme with id {meme_id} not found")
    return db_meme
