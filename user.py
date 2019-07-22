from datetime import date

from database import CursorFromConnectionPool


def save_measurements(name, weight):
    check_user_exists(name)
    with CursorFromConnectionPool() as cursor:
        cursor.execute('INSERT INTO {} (date, weight) VALUES (%s, %s)'.format(name), (date.today(), weight,))

def check_user_exists(name):
    with CursorFromConnectionPool() as cursor:
        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)', (name,))
        user_exists = cursor.fetchone()[0]
        if not user_exists:
            create_new_user(name)

def create_new_user(name):
    with CursorFromConnectionPool() as cursor:
        height = input('How tall are you? (in centimeters) ')
        cursor.execute('INSERT INTO users (name, height) VALUES (%s, %s)', (name, height))
        cursor.execute('CREATE TABLE {} (id serial, date date, weight numeric)'.format(name))

def check_users_table_exists():
    with CursorFromConnectionPool() as cursor:
        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)', ('users',))
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            cursor.execute('CREATE TABLE public.users (id serial PRIMARY KEY, name char (255), height integer)')
