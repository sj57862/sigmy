from .database import Base

class User(Base):
    __tablename__ = 'users'

class Trainer(Base):
    __tablename__ = 'trainers'

class TrainerStudiumCon(Base):
    __tablename__ = 'trainers_studium_connection'

class Studium(Base):
    __tablename__ = 'studiums'

class StudiumTrainers(Base):
    __tablename__ = 'studium_trainers'