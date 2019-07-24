from unittest import TestCase, mock
from datetime import date, timedelta

import user_functions
from database import Database, CursorFromConnectionPool


class UserFunctionsTest(TestCase):

    def setUp(self):
        Database.initialise(database='test-weight-app', user='postgres', password='Pass0987', host='localhost')
        with CursorFromConnectionPool() as cursor:
            cursor.execute('CREATE TABLE public.users (id serial PRIMARY KEY, name varchar (255), height integer)')

    def tearDown(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute('DROP SCHEMA public CASCADE;')
            cursor.execute('CREATE SCHEMA public;')

    @mock.patch('builtins.input', side_effect=['180'])
    def test_create_new_user(self, input):
        name = 'test_user'
        user_functions.create_new_user(name)

        with CursorFromConnectionPool() as cursor:
            cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)',
                           (name.lower(),))
            user_table_exists = cursor.fetchone()[0]
            cursor.execute('SELECT EXISTS(SELECT * FROM users WHERE name=%s)', (name.lower(),))
            user_is_in_users_table = cursor.fetchone()[0]

        self.assertTrue(user_table_exists)
        self.assertTrue(user_is_in_users_table)

    def test_check_users_table_exists(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute('DROP SCHEMA public CASCADE;')
            cursor.execute('CREATE SCHEMA public;')
        user_functions.check_users_table_exists()
        with CursorFromConnectionPool() as cursor:
            cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='users')")
            table_exists = cursor.fetchone()[0]

        self.assertTrue(table_exists)

    @mock.patch('builtins.input', side_effect=['175'])
    def test_save_measurements_first_time_that_day(self, input):
        name = 'Test'
        weight = 88.5
        user_functions.create_new_user(name)

        user_functions.save_measurements(name, weight)

        with CursorFromConnectionPool() as cursor:
            cursor.execute('SELECT EXISTS(SELECT * FROM {} WHERE date=%s)'.format(name), (date.today(),))
            exists = cursor.fetchone()[0]
        self.assertTrue(exists)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=['175'])
    def test_save_measurements_second_time_that_day(self, input, mock_print):
        name = 'Test'
        weight = 88.5

        user_functions.save_measurements(name, weight)
        user_functions.save_measurements(name, weight)

        output = mock_print.call_args[0][0]

        self.assertEqual(output, 'You have already saved your weight today. Come back tomorrow! :-) ')

    @mock.patch('builtins.input', side_effect=['175'])
    def test_calculate_bmi(self, input):
        name = 'Test'
        weight = 88.5
        user_functions.save_measurements(name, weight)

        bmi = user_functions.calculate_bmi(name)

        self.assertEqual(bmi, '28.90')

    def test_interpret_bmi(self):
        bmi1 = user_functions.interpret_bmi(16.5)
        bmi2 = user_functions.interpret_bmi(25)
        bmi3 = user_functions.interpret_bmi(39.99)

        self.assertEqual(bmi1, "You are underweight. You should gain weight. ")
        self.assertEqual(bmi2, "You are overweight. Think about loosing some weight. ")
        self.assertEqual(bmi3, "You are severely obese (obese class II). You should loose some weight and contact with doctor. ")

    @mock.patch('builtins.input', side_effect=['175'])
    def test_calculate_difference_if_user_is_new(self, input):
        name = 'Test'
        weight = 88.5
        user_functions.save_measurements(name, weight)

        output = user_functions.calculate_difference(name)

        self.assertEqual(output, "Welcome in weight-app! Your weight is saved. ")

    @mock.patch('builtins.input', side_effect=['175'])
    def test_calculate_difference(self, input):
        name = 'Test'
        weight = 88.5
        user_functions.save_measurements(name, weight)

        old_date = date.today() - timedelta(days=7)
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO {} (date, weight) VALUES (%s, %s)'.format(name), (old_date, 86.5))

        output = user_functions.calculate_difference(name)

        self.assertEqual(output, "You have gained 2.0 kg since last time. ")
