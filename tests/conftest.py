"""
Pytest configuration and shared fixtures for the FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture to provide a TestClient instance for making HTTP requests."""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Fixture to reset activities to a known state before each test.
    This ensures tests don't interfere with each other by providing a clean slate.
    """
    # Define a fresh copy of activities with predictable state
    fresh_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Tuesdays and Saturdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu", "james@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Learn instruments and perform in ensemble groups",
            "schedule": "Mondays and Fridays, 4:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["ava@mergington.edu", "mason@mergington.edu"]
        }
    }

    # Replace the global activities dict with our fresh copy
    monkeypatch.setitem(activities, "Chess Club", fresh_state["Chess Club"])
    monkeypatch.setitem(activities, "Programming Class", fresh_state["Programming Class"])
    monkeypatch.setitem(activities, "Gym Class", fresh_state["Gym Class"])
    monkeypatch.setitem(activities, "Basketball Team", fresh_state["Basketball Team"])
    monkeypatch.setitem(activities, "Tennis Club", fresh_state["Tennis Club"])
    monkeypatch.setitem(activities, "Art Studio", fresh_state["Art Studio"])
    monkeypatch.setitem(activities, "Music Ensemble", fresh_state["Music Ensemble"])
    monkeypatch.setitem(activities, "Debate Club", fresh_state["Debate Club"])
    monkeypatch.setitem(activities, "Science Club", fresh_state["Science Club"])

    return activities
