import datetime

class Trade:
    def __init__(self, date, type, qty, price, brokerage, is_drp=False) -> None:
        day, month, year = [int(x) for x in date.split("/")]
        self.date = datetime.date(year=year, month=month, day=day)
        self.type = type.upper()
        self.qty = int(qty)
        self.unit_price = self.clean_money(price)
        self.brokerage = self.clean_money(brokerage)
        self.price = self.unit_price * self.qty + self.brokerage
        self.is_drp = is_drp == "Y"

    def clean_money(self, n):
        return float(n.replace("$", "").replace("AU", ""))

    def __str__(self):
        return f'{self.date}: {self.type} {self.qty} at ${self.unit_price} with ${self.brokerage} brokerage for ${self.price}'
