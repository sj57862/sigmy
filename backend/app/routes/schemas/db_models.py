from .database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(100),nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    first_name = Column(String(50),nullable=True)
    last_name = Column(String(50),nullable=True)
    account_activated = Column(Boolean,nullable=True)

    trainer = relationship("Trainer",back_populates="user")

class Trainer(Base):
    __tablename__ = 'trainers'

    id = Column(Integer,primary_key=True,index=True)

    user_id = Column(Integer,ForeignKey('users.id'),unique=True)

    user = relationship("User",back_populates="trainer")

class TrainerStudiumCon(Base):
    __tablename__ = 'trainers_studium_connection'

    id = Column(Integer,primary_key=True,index=True)

class Studium(Base):
    __tablename__ = 'studiums'

    id = Column(Integer,primary_key=True,index=True)

class StudiumTrainers(Base):
    __tablename__ = 'studium_trainers'

    id = Column(Integer,primary_key=True,index=True)