import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Wikipedia Word-Frequency API! Go to /docs for API documentation."}

def test_get_word_frequency():
    response = client.get("/word-frequency?article=Soda&depth=1")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "word_counts" in data
    assert "word_percentages" in data

def test_post_keywords():
    payload = {
        "article": "Soda",
        "depth": 1,
        "ignore_list": ["python", "programming"],
        "percentile": 80
    }
    response = client.post("/keywords", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "filtered_word_counts" in data
    assert "word_percentages" in data
    assert "filtered_word_counts" in data

def test_article_not_found():
    response = client.get("/word-frequency?article=NonexistentArticle&depth=1")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Article 'NonexistentArticle' does not exist on Wikipedia."

