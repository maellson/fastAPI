from fastapi import Depends
from app.db.connection import Session
from fastapi.security import OAuth2PasswordBearer
from app.auth_user import UserUseCases
from sqlalchemy.orm import Session as sql_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def get_db_session():
    try:
        db_session = Session()
        yield db_session
    finally:
        db_session.close()


def token_verification(
        db_session: sql_session = Depends(get_db_session),
        token=Depends(oauth2_scheme)
):
    uc = UserUseCases(db_session=db_session)
    uc.verify_token(access_token=token)
