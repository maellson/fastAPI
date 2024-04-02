from sqlalchemy import Column, String, Integer, DateTime
from app.db.base import Base

# uma classe chamada "UserModel" que herda da classe "Base".


class UserModel(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True,
                nullable=False, autoincrement=True)
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)


class LoginLogModel(Base):
    __tablename__ = 'login_logs'
    id = Column('id', Integer, primary_key=True,
                nullable=False, autoincrement=True)
    username = Column('username', String, nullable=False)
    timestamp = Column('timestamp', DateTime, nullable=False)
