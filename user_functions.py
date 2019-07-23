from datetime import date

from database import CursorFromConnectionPool


def save_measurements(name, weight):
    check_user_exists(name)
    with CursorFromConnectionPool() as cursor:
        cursor.execute('INSERT INTO {} (date, weight) VALUES (%s, %s)'.format(name.lower()), (date.today(), weight,))

def check_user_exists(name):
    with CursorFromConnectionPool() as cursor:
        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)', (name.lower(),))
        user_exists = cursor.fetchone()[0]
        if not user_exists:
            create_new_user(name)

def create_new_user(name):
    with CursorFromConnectionPool() as cursor:
        height = input('How tall are you? (in centimeters) ')
        cursor.execute('INSERT INTO users (name, height) VALUES (%s, %s)', (name.lower(), height))
        cursor.execute('CREATE TABLE {} (id serial, date date, weight numeric)'.format(name.lower()))

def check_users_table_exists():
    with CursorFromConnectionPool() as cursor:
        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)', ('users',))
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            cursor.execute('CREATE TABLE public.users (id serial PRIMARY KEY, name varchar (255), height integer)')

def calculate_bmi(name):
    with CursorFromConnectionPool() as cursor:
        cursor.execute('SELECT weight FROM {} ORDER BY date DESC'.format(name.lower()))
        weight = cursor.fetchone()[0]
        cursor.execute('SELECT height FROM users WHERE name=%s', (name.lower(),))
        height = cursor.fetchone()[0]
    height = height / 100
    bmi = float(weight) / (height ** 2)
    return '%.2f' % bmi

def interpret_bmi(bmi):
    bmi = float(bmi)
    if bmi <= 16:
        return "You are severely underweight. You should contact with doctor and gain weight. "
    elif 16 < bmi < 18.5:
        return "You are underweight. You should gain weight. "
    elif 18.5 <= bmi < 25:
        return "You have normal, healthy weight. Congratulations! "
    elif 25 <= bmi < 30:
        return "You are overweight. Think about loosing some weight. "
    elif 30 <= bmi < 35:
        return "You are moderately obese (obese class I). You should loose some weight. "
    elif 35 <= bmi < 40:
        return "You are severely obese (obese class II). You should loose some weight and contact with doctor. "
    elif 40 <= bmi:
        return "You are very severely obese (obese class III). You should loose some weight and contact with doctor. "

def calculate_difference(name):
    with CursorFromConnectionPool() as cursor:
        cursor.execute()