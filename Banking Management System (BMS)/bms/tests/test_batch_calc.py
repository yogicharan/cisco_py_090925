import pytest
from app import create_app
from app.config import Config
from app.db import init_db, get_db
from app.models import Account
from app.batch_calc import total_balance_thread, total_balance_async
import asyncio


@pytest.fixture
def app(tmp_path):
    cfg = Config(SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path}/db.sqlite")
    app = create_app(cfg)
    init_db(app, cfg.SQLALCHEMY_DATABASE_URI)
    # seed some accounts
    db = get_db()
    db.add_all([Account(name=f"a{i}", number=f"n{i}", balance=i) for i in range(20)])
    db.commit()
    return app


def test_total_balance_thread(app):
    total = total_balance_thread(batch_size=5)
    # sum 0..19 = 190
    assert total == pytest.approx(190.0)


@pytest.mark.asyncio
async def test_total_balance_async(app):
    total = await total_balance_async(batch_size=7, concurrency=3)
    assert total == pytest.approx(190.0)
