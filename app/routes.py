from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.auth_user import UserUseCases
from app.schemas import User



# Cria uma instância da classe APIRouter.
router = APIRouter(prefix='/user', tags=['User'])

# Define a rota "/register" com o método HTTP POST.


@router.post('/register')
def user_register(user: User,
                  db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user)
    return JSONResponse(
        content={'msg': 'Usuário cadastrado com sucesso'},
        status_code=status.HTTP_201_CREATED
    )

# Define a rota "/login" com o método HTTP POST.
@router.post('/login')
def user_register(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
    ):
    uc = UserUseCases(db_session=db_session)
    user = User(
        username=request_form_user.username, 
        password=request_form_user.password
        )
    auth_data = uc.user_login(user=user)
    # Retorna um JSON com os dados de autenticação.
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )
