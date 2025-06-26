import uuid
import pytest

from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from databases import Database
from sqlalchemy import create_engine

from app.main import app
from app.db import metadata
import app.db as db_module


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session", autouse=True)
async def db(engine):
    test_db = Database(TEST_DB_URL)
    await test_db.connect()
    db_module.database = test_db
    yield
    await test_db.disconnect()


@pytest.mark.asyncio
async def test_register_user(db):
    unique_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    payload = {"email": unique_email, "full_name": "Test User", "password": "secret"}

    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with LifespanManager(app):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/users/register/", json=payload)

    assert response.status_code == 200, (
        f"Unexpected status code: {response.status_code}, body: {response.text}"
    )
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
