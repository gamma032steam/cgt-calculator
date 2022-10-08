# cgt-calculator
CGT FIFO calculator for shares.
- Uses the FIFO method. That is, oldest shares are sold first.
- Applies brokerage to the cost base of the sale that sells the final unit of a purchase.
- Probably wrong.

## Usage

Requires a csv in the following format:
| date       | type            | unit-price | price | brokerage | is-drp                                            |
|------------|-----------------|-----|-------|-----------|---------------------------------------------------|
| dd/mm/yyyy | "BUY" or "SELL" | #    | price per unit | in $    | from a dividend reinvestment plan? "Y" or "N". Can leave blank. |

See `example.csv` for an example.

Run `python example.csv DD/MM/YYYY` to calculate the CGT owed due to a sale on DD/MM/YYYY.

