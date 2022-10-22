import pytest
from flask import Flask
from src.app import configure_routes


@pytest.fixture
def client():
    app = Flask(__name__)
    configure_routes(app)
    return app.test_client()
