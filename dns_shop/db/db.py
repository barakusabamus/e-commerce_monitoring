import sqlite3
from utils.functions import send_message
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, update
from sqlalchemy.orm import Session


# todo создавать для каждый категории отдельную таблицу
def create_table(name_table='products'):
    engine = create_engine('sqlite:///dns_shop/db/dns-shop.db')
    metadata = MetaData()

    Table(name_table, metadata,
          Column('id', Integer, primary_key=True),
          Column('title', String),
          Column('price', Integer),
          Column('date', String)
          )

    metadata.create_all(engine)


def check_from_db(title, price, date):
    engine = create_engine('sqlite:///dns_shop/db/dns-shop.db')
    metadata = MetaData()

    session = Session(bind=engine)

    products = Table('products', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('title', String),
                     Column('price', Integer),
                     Column('date', String)
                     )

    result = session.query(products).filter(products.c.title == title).first()

    if result:
        if result.price != price:
            send_message(
                f"Product has changed:"
                f"\n\n {title}"
                f"\n\nOld price: {result.price}"
                f"\nNew price: {price}"
            )
            stmt = update(products).where(products.c.title == title).values(price=price, date=date)
            session.execute(stmt)
            session.commit()

    else:
        send_message(f"New product:\n\n{title}\n\nPrice: {price}")

        new_product = products.insert().values(title=title, price=price, date=date)
        session.execute(new_product)
        session.commit()
