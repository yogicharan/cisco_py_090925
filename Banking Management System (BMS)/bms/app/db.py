from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base

SessionLocal = None
engine = None


def init_db(app, db_url: str):
    global engine, SessionLocal
    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
    SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
    Base.metadata.create_all(bind=engine)

    # attach to app so tests can import easily
    app.teardown_appcontext(close_db)


def get_db():
    global SessionLocal
    if SessionLocal is None:
        raise RuntimeError("DB not initialized. Call init_db first.")
    return SessionLocal()


def close_db(exception=None):
    global SessionLocal
    if SessionLocal:
        SessionLocal.remove()
