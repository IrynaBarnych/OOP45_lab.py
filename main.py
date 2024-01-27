from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, and_, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import insert, update, delete
import json

# Отримання логіну та паролю з об'єкта конфігурації
with open('config.json') as f:
    config = json.load(f)

db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/People'
engine = create_engine(db_url)

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    birth_date = Column(Date)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def save_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item.first_name} {item.last_name}, {item.city}, {item.country}, {item.birth_date}\n")

def apply_filter_and_save(session, filter_condition, filename):
    result = session.query(Person).filter(filter_condition).all()
    save_to_file(filename, result)
    print(f"Результати фільтрації збережено у файл {filename}")

while True:
    print("Оберіть опцію:")
    print("1. Показати всіх людей")
    print("2. Показати людей з одного міста")
    print("3. Показати людей з однієї країни")
    print("4. Показати людей за комплексним фільтром")
    print("5. Вставити новий рядок")
    print("6. Оновити рядок")
    print("7. Видалити рядок")
    print("8. Зберегти результати фільтру у файл")
    print("0. Вихід")

    option = input("Ваш вибір: ")

    if option == "0":
        break
    elif option == "1":
        result = session.query(Person).all()
    elif option == "2":
        city_filter = input("Введіть назву міста: ")
        result = session.query(Person).filter(Person.city == city_filter).all()
    elif option == "3":
        country_filter = input("Введіть назву країни: ")
        result = session.query(Person).filter(Person.country == country_filter).all()
    elif option == "4":
        city_filter = input("Введіть назву міста (або залиште порожнім, якщо не хочете фільтрувати за містом): ")
        country_filter = input("Введіть назву країни (або залиште порожнім, якщо не хочете фільтрувати за країною): ")

        complex_filter = or_(
            and_(Person.city == city_filter, Person.country == country_filter),
            and_(Person.city == city_filter, country_filter == ""),
            and_(Person.country == country_filter, city_filter == ""),
        )

        result = session.query(Person).filter(complex_filter).all()
    elif option == "5":
        insert_row(session, Person.__table__)
    elif option == "6":
        update_row(session, Person.__table__)
    elif option == "7":
        delete_row(session, Person.__table__)
    elif option == "8":
        filename = input("Введіть ім'я файлу для збереження результатів фільтру: ")
        apply_filter_and_save(session, and_(), filename)
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        continue

    for person in result:
        print(f"{person.first_name} {person.last_name}, {person.city}, {person.country}, {person.birth_date}")

session.close()
