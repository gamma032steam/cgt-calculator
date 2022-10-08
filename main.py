import csv
import sys

from trade import Trade
from collections import namedtuple
import datetime

Holding = namedtuple("trade", "date qty orig_qty unit_price brokerage")
Sale = namedtuple("sale", "date, qty orig_qty unit_price brokerage discounted")

VERBOSE = False

def sort_and_filter_before_date(trades, date):
    '''Inclusive.'''
    return sorted([t for t in trades if t.date <= date], key=lambda x: x.date)

def fifo(trades):
    holdings = []
    for i, t in enumerate(trades):
        if t.type == "BUY":
            holdings.append(Holding(t.date, t.qty, t.qty, t.unit_price, t.brokerage))
        elif t.type == "SELL":
            holdings, used = fifo_sell(holdings, t)
            if i == len(trades) - 1:
                log_sell(used, t)
        else:
            raise Exception(f"Unknown trade type '{t.type}'")

    if VERBOSE:
        for h in holdings:
            print(h)

def calculate_discount(cost_base, sell_price, discounted):
    # don't discount capital losses
    if not discounted or sell_price < cost_base:
        return 0
    else:
        return (sell_price - cost_base) * .5

def log_sell(used, trade):
    print(f'CGT for {trade}:')
    tot_cgt = 0
    tot_discount = 0
    for t in used:
        cost_base = (t.qty * t.unit_price) + t.brokerage 
        sell_price = t.qty * trade.unit_price
        cgt = sell_price - cost_base
        discount = calculate_discount(cost_base, sell_price, t.discounted)
        tot_cgt += cgt - discount
        tot_discount += discount
        print(f'Used {t.qty} of an original {t.orig_qty} of shares from {t.date}. Cost {t.qty}*{t.unit_price} plus brokerage of {t.brokerage} for {cost_base}. Sold for {t.qty}*{trade.unit_price}={sell_price}. Gained {sell_price-cost_base}, CGT of {cgt}. Discounted: {t.discounted}')
    print(f'Total capital gain from this sale: ${tot_cgt + tot_discount}. Discounted {tot_discount} for a final CGT of {tot_cgt}')

def fifo_sell(holdings, trade):
    '''Calculates the new holdings and the consumed holdings (also using the 
    holding type) of a sale.'''
    q = trade.qty
    used = []
    while q > 0:
        if len(holdings) == 0:
            raise Exception(f"Sold units you didn't have on {trade.date}")
        next = holdings.pop(0)
        # receive the CGT discount if you sell after 1 year
        discounted = trade.date >= next.date + datetime.timedelta(days=365)
        if q >= next.qty:
            # rest of the lot
            used.append(Sale(next.date, next.qty, next.orig_qty, next.unit_price, next.brokerage, discounted))
            q -= next.qty
        else:
            # part of the lot
            holdings.insert(0, Holding(next.date, next.qty - q, next.qty, next.unit_price, next.brokerage))
            used.append(Sale(next.date, q, next.orig_qty, next.unit_price, 0, discounted))
            q -= next.qty
    return holdings, used

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        trades = list(csv.reader(f, delimiter=","))[1:]
        trades = [Trade(*t[:6]) for t in trades]

        day, month, year = [int(x) for x in sys.argv[2].split("/")]
        end_date = datetime.date(year=year, month=month, day=day)
        trades = sort_and_filter_before_date(trades, end_date)

        if len(trades) == 0:
            raise Exception("There's no trades. Did you format the csv correctly?") 

        if VERBOSE:
            for t in trades:
                print(t)           
        fifo(trades)