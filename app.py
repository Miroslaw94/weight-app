import argparse

from database import Database
import user


Database.initialise(database='weight-app', user='postgres', password='Pass0987', host='localhost')

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str, metavar='', required=True, help="Your name")
parser.add_argument('-w', '--weight', type=float, metavar='', help="Your today's weight")
parser.add_argument('-g', '--graph', action='store_true', help="Creates your weight graph")
args = parser.parse_args()


if __name__ == '__main__':
    print(f"Hello {args.name}! Your today's weight is {args.weight}")
    user.check_users_table_exists()
    if args.weight:
        user.save_measurements(args.name, args.weight)
        print("Weight saved.")
    if args.graph:
        print("Graph.")
