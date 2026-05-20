import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Import after setting DATABASE_URL
os.environ["DATABASE_URL"] = SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="session")
def db():
    """Create test database"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    from config.database import Base
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(db):
    """Get database session for tests"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    """Get FastAPI test client"""
    from app.main import app
    from config.database import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
