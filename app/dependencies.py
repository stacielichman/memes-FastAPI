from app.db.base import async_session


async def get_db():
    """
    Creates a database session and closes it after finishing
    """
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
