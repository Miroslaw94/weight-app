import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str, metavar='', required=True, help="Your name")
parser.add_argument('-w', '--weight', type=float, metavar='', help="Your today's weight")
parser.add_argument('-g', '--graph', metavar='', help="Create your weight graph")
args = parser.parse_args()


if __name__ == '__main__':
    print(f"Hello {args.name}! Your today's weight is {args.weight}")
