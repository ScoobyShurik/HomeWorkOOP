import psycopg2

def create_db(conn):
    cursor = conn.cursor()
    cursor.execute('''create table if not exists client(
    id int not null,
    first_name varchar,
    last_name varchar,
    email varchar,
    CONSTRAINT client_pk PRIMARY KEY (id);
    
    create table if not exists client_contact(
    id int not null,
    phone varchar,
    client int,
    CONSTRAINT contact_pk PRIMARY KEY (id),
    CONSTRAINT contact_client_fk FOREIGN KEY (client) REFERENCES client(id) ON DELETE CASCADE ON UPDATE CASCADE;
    ''')
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    cursor = conn.cursor()
    cursor.execute(f'''
                insert into client(first_name, last_name, email) values
                ({first_name}, {last_name}, {email}) RETURNING id
                ''')
    client_id = cursor.fetchone()[0]
    if phones is not None:
        for phone in phones:
            cursor.execute(f'''
            insert into contact(phone, client) values
            ({phone}, {client_id})
            ''')
    conn.commit()

def add_phone(conn, client_id, phone):
    cursor = conn.cursor()
    cursor.execute(f'''
        insert into contact(phone, client) values
        ({phone}, {client_id})
        ''')
    conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cursor = conn.cursor()
    cursor.execute(f'''
            update client SET first_name = {first_name}, last_name = {last_name}, email = {email} WHERE id = {client_id}
            ''')
    if phones is not None:
        for phone in phones:
            cursor.execute(f'''
                update contact SET phone = {phone} where client = {client_id}
    ''')
    conn.commit()

def delete_phone(conn, client_id, phone):
    cursor = conn.cursor()
    cursor.execute(f'''
            delete contact where client = {client_id} and phone = {phone}
            ''')
    conn.commit()

def delete_client(conn, client_id):
    cursor = conn.cursor()
    cursor.execute(f'''
                delete client where id = {client_id}
                ''')
    conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cursor = conn.cursor()
    cursor.execute(f'''
                select * from client where first_name = {first_name} and last_name = {last_name} and email = {email} and id = (
                select client from contact where phone = {phone} limit 1 )
                ''')
    client = cursor.fetchone()[0]
    print(client)


with psycopg2.connect(host="localhost", port=5432, database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, "Иван", "Иванов", "ivanov@mail.com", ['88005553535', '1211'])
    add_phone(conn, 1, '5455')
    change_client(conn, 1, "Иван", "Петров", "asdf@mail.ru")
    delete_phone(conn, 1, '1211')
    delete_client(conn, 1)
    add_client(conn, "Семен", "Калугин", "ivanov@mail.com", ['88005553535', '1211'])
    find_client(conn, "Семен", "Калугин", "ivanov@mail.com", '88005553535')

conn.close()