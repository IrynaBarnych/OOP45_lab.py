from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, and_, or_
from sqlalchemy.orm import sessionmaker, declarative_base
import json  # Import the json module

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

# Додавання інформації
person1 = Person(first_name='John', last_name='Doe', city='New York', country='USA', birth_date='1990-01-15')
person2 = Person(first_name='Jane', last_name='Smith', city='London', country='UK', birth_date='1985-03-22')
session.add_all([person1, person2])
session.commit()

# Програма для виконання готових фільтрів
while True:
    print("Оберіть опцію:")
    print("1. Показати всіх людей")
    print("2. Показати людей з одного міста")
    print("3. Показати людей з однієї країни")
    print("4. Показати людей за комплексним фільтром")
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

        # Складаємо комплексний фільтр з умов АБО
        complex_filter = or_(
            and_(Person.city == city_filter, Person.country == country_filter),
            and_(Person.city == city_filter, country_filter == ""),
            and_(Person.country == country_filter, city_filter == ""),
        )

        result = session.query(Person).filter(complex_filter).all()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        continue

    for person in result:
        print(f"{person.first_name} {person.last_name}, {person.city}, {person.country}, {person.birth_date}")

session.close()
