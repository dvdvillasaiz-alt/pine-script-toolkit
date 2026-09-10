# Pine Script Toolkit

Open-source indicators for TradingView, written in Pine Script v6 — with the
arithmetic behind them shown, tested and reproducible.

Most published trading tools ask you to trust a screenshot. Every tool here ships
with the scripts that check its maths and the literal output of running them. If
a formula is claimed, the proof is in the repo.

---

## Indicators

| Indicator | What it does | Status |
|---|---|---|
| [**Risk Console**](RISK-CONSOLE.md) | Position sizing from an ATR-scaled stop, then charges the trade for commission, slippage and funding and restates every target in what is actually left | Stable |

---

## Why the verification scripts exist

A backtest with no costs is a work of fiction, and a formula in a description is
just a claim. So each indicator carries:

- **The derivation**, written out, not asserted.
- **A script that tests it numerically** — usually Monte Carlo, because a formula
  that survives 400,000 simulated trades is harder to argue with than one that
  merely looks right.
- **A degenerate-case check.** Every formula here must collapse to the textbook
  version when its extra term is zero. If it doesn't, it is wrong.
- **The literal stdout** of running those scripts, committed as [`VERIFICATION.md`](VERIFICATION.md).

Example, from Risk Console: the break-even win rate with costs is
`p = (1 + c) / (R + 1)`. With `c = 0` that must reduce to the familiar
`p = 1/(R + 1)` — and it does. Monte Carlo across nine scenarios returns an
expectancy of approximately zero at exactly the win rate the formula predicts.

---

## Highlight: what trading costs really do to you

Cost drag is driven by position size, and position size is inversely proportional
to stop distance. Halve your stop and you double your size, which doubles your
commission — while your 1R stays exactly the same.

Round-trip cost as a share of 1R (BTC/EUR, ATR 900, 2 ticks slippage per side):

| Stop | 0.05% / side | 0.10% / side |
|---|---|---|
| 0.25 × ATR | 26.8% | **53.5%** |
| 0.50 × ATR | 13.4% | 26.8% |
| 1.00 × ATR | 6.7% | 13.4% |
| 2.00 × ATR | 3.4% | 6.7% |

At a 0.25 ATR stop and 0.10% per side, a 2R target needs a **51.2%** win rate
rather than the 33.3% the textbook promises — 17.8 percentage points paid
entirely to your broker. This is the arithmetic reason tight-stop scalping is
hard, and it is invisible in a zero-cost backtest.

Numbers reproducible with [`sensitivity.py`](sensitivity.py).

---

## Using these

1. Open TradingView, then the **Pine Editor** at the bottom of any chart.
2. Paste the contents of the `.pine` file.
3. **Add to chart**.
4. If the panel renders behind the candles, right-click the indicator →
   *Visual order* → *Bring to front*. That is a chart-level setting, not a bug in
   the script.

Requires Pine Script v6. No external dependencies, no `request.security`, no
repainting.

---

## Work with me / Trabajo por encargo

I build custom indicators and strategies in Pine Script: new tools from a spec,
modifications to existing scripts, alert and webhook plumbing, and auditing
backtests for look-ahead bias and unrealistic cost assumptions.

Construyo indicadores y estrategias a medida en Pine Script para TradingView:
herramientas nuevas a partir de una especificación, modificaciones de scripts
existentes, alertas y webhooks, y auditoría de backtests para detectar
look-ahead bias y supuestos de coste poco realistas. Atiendo en español y en
inglés.

**Contact:** open an issue in this repository.

---

## Disclaimer

Nothing here is financial advice or a recommendation to trade any instrument.
These are calculators and analysis tools; none of them generates buy or sell
signals. Costs are modelled from the inputs you supply, not fetched from any
exchange — the output is only as honest as what you type in.

## License

[Mozilla Public License 2.0](LICENSE), matching the default licence TradingView
applies to Pine Script publications.
