# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config 

from app.main import app
from app.db.database import Base, get_db
# from app.services.rabbitmq import RabbitMQService

# Setup environment for testing
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:2Dx1wZYn72kiWMrYog6R@database-1.cw1s0reh8nwq.us-east-2.rds.amazonaws.com:5432/cowryrise_db")

# Create a new SQLAlchemy engine for the test database
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency for the database in FastAPI
@pytest.fixture(scope="module")
def db():
    # Apply migrations before starting tests
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
    # Create a new session for the test database
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

    # After tests, you can optionally clean up the database
    command.downgrade(alembic_cfg, "base")

# Override FastAPI's default dependency injection to use the test database
@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

# Mock RabbitMQ for testing
# @pytest.fixture(scope="module")
# def mock_rabbitmq(monkeypatch):
#     class MockRabbitMQService:
#         def publish_message(self, message: str):
#             # Mock implementation for testing
#             print(f"Mock publish: {message}")

#         def consume_message(self, callback):
#             # Mock consume function
#             callback("Mock message")

#     # Override the actual RabbitMQ service with the mock version
#     monkeypatch.setattr(RabbitMQService, "publish_message", MockRabbitMQService().publish_message)
#     monkeypatch.setattr(RabbitMQService, "consume_message", MockRabbitMQService().consume_message)

#     yield MockRabbitMQService()

