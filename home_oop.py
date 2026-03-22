from datetime import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.sqltypes import Numeric

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/book_db"


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    publisher_id = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    stocks = relationship('Stock', back_populates='shop')


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)

    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(10, 2), nullable=False)
    date_sale = Column(DateTime, default=datetime.now, nullable=False)
    stock = relationship('Stock', back_populates='sales')
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer)


def create_engine_and_session():
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def add_sample_data(session):
    if session.query(Publisher).count() > 0:
        return

    publishers = [
        Publisher(name='Эксмо'),
        Publisher(name='АСТ'),
        Publisher(name='Просвещение'),
    ]
    session.add_all(publishers)
    session.commit()

    books = [
        Book(name='Капитанская дочка', publisher_id=publishers[0].id),
        Book(name='Руслан и Людмила', publisher_id=publishers[0].id),
        Book(name='Евгений Онегин', publisher_id=publishers[1].id),
        Book(name='Война и мир', publisher_id=publishers[2].id),
    ]
    session.add_all(books)
    session.commit()

    shops = [
        Shop(name='Буквоед'),
        Shop(name='Лабиринт'),
        Shop(name='Книжный дом'),
    ]
    session.add_all(shops)
    session.commit()

    stocks = [
        Stock(id_book=books[0].id, id_shop=shops[0].id, count=10),
        Stock(id_book=books[0].id, id_shop=shops[1].id, count=5),
        Stock(id_book=books[1].id, id_shop=shops[0].id, count=8),
        Stock(id_book=books[2].id, id_shop=shops[2].id, count=3),
    ]
    session.add_all(stocks)
    session.commit()


    from datetime import timedelta
    sales = [
        Sale(price=600.00, date_sale=datetime(2022, 11, 9), id_stock=stocks[0].id),
        Sale(price=500.00, date_sale=datetime(2022, 11, 8), id_stock=stocks[2].id),
        Sale(price=580.00, date_sale=datetime(2022, 11, 5), id_stock=stocks[1].id),
        Sale(price=490.00, date_sale=datetime(2022, 11, 2), id_stock=stocks[3].id),
        Sale(price=600.00, date_sale=datetime(2022, 10, 26), id_stock=stocks[0].id),
    ]
    session.add_all(sales)
    session.commit()


def get_sales_by_publisher(session, publisher_input):
    try:
        publisher_id = int(publisher_input)
        publisher = session.query(Publisher).filter_by(id=publisher_id).first()
        if publisher:
            publisher_name = publisher.name
        else:
            publisher = session.query(Publisher).filter(
                Publisher.name.ilike(f'%{publisher_input}%')
            ).first()
            if not publisher:
                return None, []
            publisher_name = publisher.name
    except ValueError:
        publisher = session.query(Publisher).filter(
            Publisher.name.ilike(f'%{publisher_input}%')
        ).first()
        if not publisher:
            return None, []
        publisher_name = publisher.name
    results = session.query(
        Book.name.label('book_name'),
        Shop.name.label('shop_name'),
        Sale.price,
        Sale.date_sale
    ).join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id_stock == Stock.id) \
        .filter(Book.publisher_id == publisher.id) \
        .order_by(Sale.date_sale.desc()) \
        .all()

    return publisher_name, results


def format_output(publisher_name, results):
    if not results:
        print(f"\nПо издателю '{publisher_name}' продаж не найдено")
        return

    print(f"\nПродажи книг издательства '{publisher_name}':")
    print("=" * 70)
    print(f"{'Название книги':<30} | {'Магазин':<15} | {'Цена':>8} | {'Дата'}")
    print("-" * 70)

    for book_name, shop_name, price, date_sale in results:
        date_str = date_sale.strftime('%d-%m-%Y') if date_sale else 'N/A'
        price_str = f"{price:.2f}".rstrip('0').rstrip('.')
        print(f"{book_name:<30} | {shop_name:<15} | {price_str:>8} | {date_str}")
    print("=" * 70)
    print(f"Всего найдено продаж: {len(results)}")

def main():
    print("Поиск продаж по издателю")
    print("-" * 40)

    try:
        session = create_engine_and_session()
        add_sample_data(session)
        publisher_input = input("\nВведите имя или ID издателя: ").strip()
        if not publisher_input:
            print("Ввод не может быть пустым")
            return
        publisher_name, results = get_sales_by_publisher(session, publisher_input)
        if publisher_name is None:
            print(f"\nИздатель '{publisher_input}' не найден в базе")
            return
        format_output(publisher_name, results)

    except SQLAlchemyError as e:
        print(f"\nОшибка базы данных: {e}")
    except Exception as e:
        print(f"\nОшибка: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    main()