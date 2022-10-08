# cgt-calculator
CGT FIFO calculator for shares.
- Uses the FIFO method. That is, oldest shares are sold first.
- Applies brokerage to the cost base of the sale that sells the final unit of a lot.
- CGT discount aware.
- Doesn't support multiple trades per day.
- Probably wrong.

## Usage

Requires a csv in the following format:
| date       | type            | qty | unit-price | brokerage 
|------------|-----------------|-----|-------|-----------|
| dd/mm/yyyy | "BUY" or "SELL" | #    | price per unit | in $   

See `example.csv` for an example.

Run `python example.csv 01/09/2022` to calculate the CGT owed due to a sale on 01/09/2022:
```
CGT for 2022-09-01: SELL 4 at $300.0 with $0.0 brokerage for $1200.0:
Used 2 of an original 5 of shares from 2021-01-01. Cost 2*100.0 plus brokerage of 5.0 for 205.0. Sold for 2*300.0=600.0. Gained 395.0, CGT of 197.5. Discounted: True
Used 1 of an original 1 of shares from 2022-07-01. Cost 1*100.0 plus brokerage of 5.0 for 105.0. Sold for 1*300.0=300.0. Gained 195.0, CGT of 195.0. Discounted: False
Used 1 of an original 5 of shares from 2022-08-01. Cost 1*200.0 plus brokerage of 0 for 200.0. Sold for 1*300.0=300.0. Gained 100.0, CGT of 100.0. Discounted: False
Total capital gain from this sale: $690.0. Discounted 197.5 for a final CGT of 492.5
```

