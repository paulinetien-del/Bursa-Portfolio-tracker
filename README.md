# Bursa Portfolio Tracker

A free, single-page portfolio tracker for Bursa Malaysia stocks: watchlist, trades, holdings, and pie charts by stock and by sector. It runs on GitHub Pages.

- **Prices:** Yahoo Finance end-of-day closes, refreshed Mon–Fri at 6:37pm MYT by a GitHub Action that updates `prices.json`.
- **Investor data:** each person's trades, watchlist and plan stay in their own browser (localStorage). They can use **Plan → Backup** to export a file or move to another device. No sign-up, no server.

## Files
| File | What it is |
|---|---|
| `index.html` | The whole app |
| `prices.json` | Latest prices (written by the Action) |
| `symbols.txt` | Stocks the Action prices, one Yahoo code per line (e.g. `7106.KL`) |
| `scripts/fetch_prices.py` | The price fetcher |
| `.github/workflows/update-prices.yml` | Daily schedule |

## Adding a stock
Add its code to `symbols.txt` (e.g. `7106.KL`) and commit. It gets a price after the next run, or right away if you run the Action by hand (Actions → Update prices → Run workflow).

## Not investment advice
For tracking and education only.
