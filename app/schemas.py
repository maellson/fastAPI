import re
from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_alphanumeric(cls, value):
        if not re.match(
            r"^[a-zA-Z0-9_@]{8,20}$",
            value
        ):
            raise ValueError(
                "Username deve ser alfanumérico ou _ e @, não pode conter espaços, "
                "deve ser maior do que 8 caracteres e menor do que 20 caracteres"
            )
        return value
