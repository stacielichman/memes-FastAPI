import json
from io import BytesIO
from typing import Optional

import pytest
from app.main import app
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel


class MemeCreateTestData(BaseModel):
    """
    Test data for creating a meme.
    """
    title: str = "Test Meme"
    description: Optional[str] = "This is a test meme"


class MemeUpdateTestData(BaseModel):
    """
    Test data for updating a meme.
    """
    title: str = "Updated Meme"


meme_create_test_data = MemeCreateTestData().model_dump()
meme_update_test_data = MemeUpdateTestData().model_dump()


@pytest.mark.asyncio
async def test_get_memes():
    """
    Test gets all memes
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/memes/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0
        await ac.aclose()


@pytest.mark.asyncio
async def test_get_meme():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/memes/1")
        assert response.status_code == 404
        assert response.json() == {'detail': 'Item not found'}
        await ac.aclose()


@pytest.mark.asyncio
async def test_post_meme():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        file = BytesIO(b"test file content")
        file.name = "test.jpg"
        response = await ac.post("/memes/",
                                 data={'meme': json.dumps(meme_create_test_data)},
                                 files={"file": (file.name, file, 'image/jpeg')})
        assert response.status_code == 200
        assert response.json()["title"] == meme_create_test_data["title"]
        assert response.json()["description"] == meme_create_test_data["description"]
        assert "image_url" in response.json()
        await ac.aclose()


@pytest.mark.asyncio
async def test_update_meme():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/memes/12", json=meme_update_test_data)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Meme"


@pytest.mark.asyncio
async def test_delete_meme():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete("/memes/12")
        assert response.status_code == 200
