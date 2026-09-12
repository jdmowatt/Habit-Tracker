import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

# Separate test-only database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_habit():
    response = client.post("/habits", json={"name": "Drink water"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Drink water"
    assert "id" in data

def test_get_habits_empty():
    response = client.get("/habits")
    assert response.status_code == 200
    assert response.json() == []

def test_get_nonexistent_habit():
    response = client.get("/habits/999")
    assert response.status_code == 404

def test_delete_habit():
    create_response = client.post("/habits", json={"name": "Read"})
    habit_id = create_response.json()["id"]

    delete_response = client.delete(f"/habits/{habit_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/habits/{habit_id}")
    assert get_response.status_code == 404


def test_streak_zero_with_no_completions():
    create_response = client.post("/habits", json={"name": "Exercise"})
    habit_id = create_response.json()["id"]

    streak_response = client.get(f"/habits/{habit_id}/streak")
    assert streak_response.json()["streak"] == 0

def test_streak_counts_consecutive_days():
    from datetime import date, timedelta

    create_response = client.post("/habits", json={"name": "Meditate"})
    habit_id = create_response.json()["id"]

    today = date.today()
    for i in range(3):
        d = today - timedelta(days=i)
        client.post(f"/habits/{habit_id}/complete", json={"completed_date": d.isoformat()})

    streak_response = client.get(f"/habits/{habit_id}/streak")
    assert streak_response.json()["streak"] == 3