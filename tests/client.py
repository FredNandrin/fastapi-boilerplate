from fastapi.testclient import TestClient
from app.api import app
from app.database._connection import client


client = TestClient(app)
