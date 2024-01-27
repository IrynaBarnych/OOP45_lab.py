from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, and_, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import insert, update, delete
import json  # Add this line to import the json module

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/People'
engine = create_engine(db_url)

# Оголошення базового класу
Base = declarative_base()

# Визначення класу моделі
class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    birth_date = Column(Date)

# Створення таблиці
Base.metadata.create_all(engine)

# Створення сесії та додавання запису
Session = sessionmaker(bind=engine)
session = Session()

# Функції для вставки, оновлення та видалення записів
def insert_row(session, table):
    columns = table.columns.keys()

    values = {}
    for column in columns:
        value = input(f"Введіть значення для колонки {column}: ")
        values[column] = value

    session.execute(insert(table).values(values))
    session.commit()

    print("Рядок успішно додано!")

def update_row(session, table):
    columns = table.columns.keys()
    print("Доступні колонки для оновлення: ")
    for idx, column in enumerate(columns, start=1):
        print(f"{idx}.{column}")
    selected_column_idx = int(input("Введіть номер колонки для оновлення: "))

    if 1 <= selected_column_idx <= len(columns):
        condition_column = columns[selected_column_idx - 1]
    else:
        print("Невірний номер колонки!")

    condition_value = input(f"Введіть значення для умови, {condition_column}: ")
    new_values = {}
    for column in columns:
        value = input(f"Введіть значення для колонки {column}: ")
        new_values[column] = value

    confirm_update = input("Оновити усі рядки? у/н? ")
    if confirm_update.lower() == 'y':
        session.execute(update(table).where(getattr(table.c, condition_column) == condition_value).values(new_values))
        session.commit()
        print("Рядок(и) успішно оновлено!")

def delete_row(session, table):
    columns = table.columns.keys()
    print("Доступні колонки для видалення: ")
    for idx, column in enumerate(columns, start=1):
        print(f"{idx}.{column}")
    selected_column_idx = int(input("Введіть номер колонки для умови видалення: "))

    if 1 <= selected_column_idx <= len(columns):
        condition_column = columns[selected_column_idx - 1]
    else:
        print("Невірний номер колонки! Видалення відмінено!")

    condition_value = input(f"Введіть значення для умови, {condition_column}: ")

    confirm_delete = input("Видалити усі рядки з цієї таблиці? у/н? ")
    if confirm_delete.lower() == 'y':
        session.execute(delete(table).where(getattr(table.c, condition_column) == condition_value))
        session.commit()
        print("Рядок(и) успішно видалено!")

# Головний цикл програми
while True:
    print("Оберіть опцію:")
    print("1. Показати всіх людей")
    print("2. Показати людей з одного міста")
    print("3. Показати людей з однієї країни")
    print("4. Показати людей за комплексним фільтром")
    print("5. Вставити новий рядок")
    print("6. Оновити рядок")
    print("7. Видалити рядок")
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
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        continue

    for person in result:
        print(f"{person.first_name} {person.last_name}, {person.city}, {person.country}, {person.birth_date}")

session.close()
