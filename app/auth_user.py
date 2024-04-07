from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from app.db.models import UserModel
from app.schemas import User

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
