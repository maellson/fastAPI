from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = config('DB_URL')

engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


def connect_to_database():
    """
    Connects to the database using the provided DB_URL and returns a session object.

    Returns:
        Session: A session object that can be used to interact with the database.
    """
    return Session()
