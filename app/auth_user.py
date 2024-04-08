from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from app.db.models import UserModel
from app.schemas import User

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

# A classe CryptContext é usada para criptografar e verificar senhas.
crypt_context = CryptContext(schemes=['sha256_crypt'])

# A classe UserUseCases é responsável por manipular os dados do usuário.
# Ela garantira junto com o controle de rotas - routes.py e o controle de dependencias - depends.py que
# o usuário seja cadastrado e verificado na base de dados, mas que apenas uma sessão seja criada para o mesmo.


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # O método "user_register" é responsável por cadastrar e verificar se o usuário existe na base de dados.
    def user_register(self, user: User):
        user_model = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        try:
            # Adiciona o objeto "user_model" ao banco de dados.
            self.db_session.add(user_model)
            # Salva as alterações no banco de dados.
            self.db_session.commit()
        # Se o usuário já existir na base de dados, uma exceção será lançada.
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User já existe na base de dados'
            )

    def user_login(self, user: User, expires_in: int = 30):
        user_model = self.db_session.query(UserModel).filter_by(
            username=user.username
        ).first()
        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User não encontrado'
            )
        if not crypt_context.verify(user.password, user_model.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Senha incorreta'
            )
        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': user_model.username,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token):
        try:
            payload = jwt.decode(access_token, SECRET_KEY,
                                 algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token inválido'
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido'
            )
        user = self.db_session.query(UserModel).filter_by(
            username=username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User não encontrado'
            )
