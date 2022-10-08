import csv
import sys
from trade import Trade

def filter_before_date(trades, date):
    ''''''

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        trades = list(csv.reader(f, delimiter=","))[1:]
        trades = [Trade(*t) for t in trades]
        for t in trades:
            print(t)