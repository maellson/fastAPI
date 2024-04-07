from app.db.connection import Session


def get_db_session():
    try:
        db_session = Session()
        yield db_session
    finally:
        db_session.close()
