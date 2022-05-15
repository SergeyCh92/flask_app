from email.policy import default
from psycopg2 import Timestamp
from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


Base = declarative_base()


class DbClient:
    def __init__(self, connection: str):
        self.engine = create_engine(connection)
        self.Base = declarative_base()
        self.session = scoped_session(sessionmaker(bind=self.engine))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String(100), nullable=False)
    create_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref="users")
