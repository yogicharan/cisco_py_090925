import pytest
from app import create_app
from app.config import Config
from app.db import init_db, get_db
from app.models import Base, Account
import tempfile
import os


@pytest.fixture
def app(tmp_path):
    db_file = tmp_path / "test.sqlite"
    cfg = Config(SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_file}")
    app = create_app(cfg)
    # re-init DB for tests
    init_db(app, cfg.SQLALCHEMY_DATABASE_URI)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_create_and_get_account(client):
    resp = client.post("/api/accounts", json={"name": "Alice", "number": "ACC123", "balance": 50.0})
    assert resp.status_code == 201
    payload = resp.get_json()
    assert payload["name"] == "Alice"
    assert payload["balance"] == 50.0

    acc_id = payload["id"]
    resp2 = client.get(f"/api/accounts/{acc_id}")
    assert resp2.status_code == 200
    p2 = resp2.get_json()
    assert p2["number"] == "ACC123"


def test_list_and_delete(client):
    client.post("/api/accounts", json={"name": "A", "number": "N1", "balance": 10})
    client.post("/api/accounts", json={"name": "B", "number": "N2", "balance": 20})
    r = client.get("/api/accounts")
    assert len(r.get_json()) >= 2
