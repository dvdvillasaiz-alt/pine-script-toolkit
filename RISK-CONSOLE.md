# Risk Console — ATR Position Sizing & Cost Impact

Position sizing that does not stop at "how many units". It charges the trade for
commission, slippage and funding, then restates every target in what is actually
left.

---

## The problem it solves

Your risk and your costs come out of the same pocket. A 2R winner is not a 2R
winner once the round trip is paid for — and almost nobody checks by how much.

Most position-size calculators tell you the units and stop there. This one asks
the question after that: given what you are actually paying to get in and out,
what win rate does this setup now need?

---

## What it shows

**Setup** — entry (current close, or a price you type in); the stop from one of
three methods (ATR multiple, percent of price, or a manual price); position size
in units, notional exposure, and 1R in your account currency.

**Real costs, round trip** — commission charged on entry *and* exit; slippage in
ticks per side, so it scales with the instrument's tick size; funding or carry
across the expected hold, for perps and CFDs; the total, and that total as a
share of 1R, colour-coded.

**After costs** — each R target as a price, the net R once the round trip is
paid for, and the break-even win rate you need at that target.

---

## The formula

For a target of `R` and a round-trip cost of `c`, both in R units:

- A winner nets `R − c`
- A loser costs `1 + c`

```
E = p·(R − c) − (1 − p)·(1 + c) = p·(R + 1) − (1 + c)
```

Setting expectancy to zero:

```
p = (1 + c) / (R + 1)
```

With `c = 0` this collapses to the familiar `p = 1/(R + 1)`. The gap between the
two is the entire point of the tool.

Verified numerically in [`verify_math.py`](verify_math.py) — Monte Carlo over
400,000 trades per scenario, nine scenarios, expectancy ≈ 0 at exactly the win
rate the formula predicts. See [`VERIFICATION.md`](VERIFICATION.md) for the
raw output.

---

## Why stop distance is the lever

Cost drag is driven by position size, and position size is inversely
proportional to stop distance. Halve the stop, double the size, double the
commission — while 1R stays identical.

BTC/EUR, ATR 900, 2 ticks slippage per side. Round-trip cost as a share of 1R:

| Stop | 0.05% / side | 0.10% / side |
|---|---|---|
| 0.25 × ATR | 26.8% | **53.5%** |
| 0.50 × ATR | 13.4% | 26.8% |
| 1.00 × ATR | 6.7% | 13.4% |
| 2.00 × ATR | 3.4% | 6.7% |

Win rate needed at a 2R target:

| Stop, commission | Textbook | With costs | Difference |
|---|---|---|---|
| 0.25 ATR, 0.10% | 33.3% | **51.2%** | +17.8 pp |
| 0.50 ATR, 0.10% | 33.3% | 42.3% | +8.9 pp |
| 1.00 ATR, 0.05% | 33.3% | 35.6% | +2.2 pp |
| 2.00 ATR, 0.05% | 33.3% | 34.5% | +1.1 pp |

---

## How to use it

1. Enter your real account size and the percentage you risk per trade.
2. Set commission to your venue's **taker** fee for one side. The script doubles it.
3. Set slippage honestly. Two ticks is optimistic on anything but the deepest
   books, and much too optimistic around scheduled news.
4. For perps, enter your expected **total** funding across the hold. For spot,
   leave it at zero.
5. Read **Cost vs 1R**. Under 15% is workable, 15–30% deserves a second look,
   over 30% means the setup is mostly paying your broker.

The panel follows your chart theme automatically. If it renders behind the
candles, right-click the indicator → *Visual order* → *Bring to front*; that is
a chart-level setting, not a bug.

---

## Limitations, stated plainly

- This is a calculator, not a signal generator. It never says buy or sell.
- Costs are modelled from your inputs, not fetched from any exchange. The output
  is only as honest as what you type in.
- Slippage is treated as symmetric and constant. In reality it is worse on
  exits, worse in thin books, and much worse on news.
- Funding is one total figure for the whole hold rather than accrued per
  interval, which keeps it usable without assuming a holding period.
- Position size assumes fractional units. Round down to your venue's minimum
  order increment before trading.
- Values update on the most recent bar and use the current close unless you set
  a manual entry.

## Does it repaint?

No. There is no `request.security`, no lookahead, and no backward-shifted
series. Everything is computed on the current bar inside `barstate.islast`.
