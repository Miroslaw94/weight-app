import argparse

from database import Database
import user_functions


Database.initialise(database='weight-app', user='postgres', password='Pass0987', host='localhost')

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str, metavar='', required=True, help="Your name. ")
parser.add_argument('-w', '--weight', type=float, metavar='', help="Your today's weight. ")
parser.add_argument('-b', '--bmi', action='store_true', help="Calculates your BMI. ")
parser.add_argument('-g', '--graph', type=str, metavar='', help="Creates your weight graph. Type 'm' after -g to see "
                                                                "your monthly weight change, type 'y' to see yearly "
                                                                "weight change, type anything to use all measurements.")
args = parser.parse_args()


if __name__ == '__main__':
    print(f"Hello {args.name}! ")
    user_functions.check_users_table_exists()
    if args.weight:
        user_functions.save_measurements(args.name, args.weight)
        print(user_functions.calculate_difference(args.name))
    if args.bmi:
        bmi = user_functions.calculate_bmi(args.name)
        print(f"Your today's BMI is {bmi}")
        print(user_functions.interpret_bmi(bmi))
    if args.graph:
        user_functions.draw_graph(args.name, args.graph.lower())
