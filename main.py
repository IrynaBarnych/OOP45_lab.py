# Створіть однотабличну базу даних People (ім’я, прізвище, місто, країна, дата народження) з однойменною
# таблицею. Напишіть програму, яка дозволяє користувачеві ввести запит і отримати результати роботи запиту.
# Підтримуйте лише SELECT як запит. Якщо ви спробуєте
# виконати інші запити, потрібно буде генерувати помилку.

from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text

import json

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/People'
engine = create_engine(db_url)

#оголошення базового класу
Base = declarative_base()
#визначення класу моделі
class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    birth_date = Column(Date)

#створення таблиці
Base.metadata.create_all(engine)

#створення сесії та додавання запису
Session = sessionmaker(bind=engine)
session = Session()
#додавання інформації
person1 = Person(first_name='John', last_name='Doe', city='New York', country='USA', birth_date='1990-01-15')
person2 = Person(first_name='Jane', last_name='Smith', city='London', country='UK', birth_date='1985-03-22')

session.add_all([person1, person2])
session.commit()
#програма для виконання select-запитів
while True:
    user_query = input("Введіть вас select-запит exit  - вихід")
    if user_query.lower() == "exit":
        break
    try:
        result = session.execute(text(user_query))
        rows = result.fetchall()
        if rows:
            print("Результат: ")
            for row in rows:
                print(row)
        else:
            print("Результат відсутній")
    except Exception as e:
        print(f"Помилка виконання запиту: {e}")
session.close()