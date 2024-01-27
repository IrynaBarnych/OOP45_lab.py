from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base

import json

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/SchoolDB'
engine = create_engine(db_url)

#оголошення базового класу
Base = declarative_base()
#визначення класу моделі
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))

#створення таблиці
Base.metadata.create_all(engine)

#створення сесії та додавання запису
Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name = "John Doe")
session.add(new_user)
session.commit()