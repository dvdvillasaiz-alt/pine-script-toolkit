"""
Independent check of the arithmetic behind the Risk Console indicator.

This does not validate Pine syntax - only TradingView's compiler can do that.
What it validates is that the formulas produce what the documentation claims,
by re-implementing them here and testing them numerically.

Run with:  python3 verify_math.py
"""
import random

# --- Test scenario: BTC/EUR, 10,000 EUR account, 1% risk -------------------
account     = 10_000.0
risk_pct    = 1.0
entry       = 60_000.0
atr         = 900.0
atr_mult    = 2.0
comm_pct    = 0.05      # per side
slip_ticks  = 2
mintick     = 0.1       # BTC/EUR on Binance
funding_pct = 0.0

stop_dist  = atr * atr_mult
stop_price = entry - stop_dist
risk_amt   = account * risk_pct / 100.0
pos_size   = risk_amt / stop_dist
notional   = pos_size * entry

comm  = notional * comm_pct / 100.0 * 2.0     # round trip: entry AND exit
slip  = pos_size * slip_ticks * mintick * 2.0
fund  = notional * funding_pct / 100.0
total = comm + slip + fund

cost_in_R = total / risk_amt
be_pct    = total / notional * 100.0

print("-- SCENARIO ------------------------------------------")
print(f"Entry {entry:,.2f} | Stop {stop_price:,.2f} | Distance {stop_dist:,.2f}")
print(f"Position size : {pos_size:.8f} units")
print(f"Notional      : {notional:,.2f}")
print(f"Risk (1R)     : {risk_amt:,.2f}")
print()
print("-- ROUND-TRIP COSTS ----------------------------------")
print(f"Commission : {comm:8.4f}")
print(f"Slippage   : {slip:8.4f}")
print(f"Funding    : {fund:8.4f}")
print(f"TOTAL      : {total:8.4f}")
print(f"Cost as % of 1R  : {cost_in_R*100:.2f} %")
print(f"Break-even move  : {be_pct:.4f} %")
print()

# --- Check 1: internal consistency of the implied exposure -----------------
implied = risk_amt / (stop_dist / entry)
assert abs(implied - notional) < 1e-6, "notional is inconsistent"
print(f"[OK] Notional consistent ({implied:,.2f})")

# --- Check 2: the required win rate formula, against Monte Carlo ------------
def win_rate_required(R, c):
    """Break-even win rate for reward R and round-trip cost c, both in R units."""
    return (1.0 + c) / (R + 1.0)

def simulate(R, c, p, n=400_000, seed=7):
    rng = random.Random(seed)
    total_R = 0.0
    for _ in range(n):
        if rng.random() < p:
            total_R += (R - c)       # win R, still pay the cost
        else:
            total_R -= (1.0 + c)     # lose 1R, and pay the cost on top
    return total_R / n               # expectancy per trade, in R

print()
print("-- MONTE CARLO VALIDATION OF THE WIN RATE FORMULA ----")
print(f"{'R':>4} {'cost(R)':>9} {'p required':>12} {'E[R]/trade':>12}  verdict")
ok = True
for R in (1.0, 2.0, 3.0):
    for c in (0.0, cost_in_R, 0.30):
        p = win_rate_required(R, c)
        exp = simulate(R, c, p)
        good = abs(exp) < 0.006       # should sit at ~0, within sampling noise
        ok = ok and good
        print(f"{R:>4.1f} {c:>9.4f} {p*100:>11.2f}% {exp:>12.5f}  {'OK' if good else 'FAIL'}")

# --- Check 3: with no costs it must collapse to the textbook formula --------
for R in (0.5, 1.0, 2.0, 3.0, 5.0):
    assert abs(win_rate_required(R, 0.0) - 1.0/(R+1.0)) < 1e-12
print("\n[OK] With zero costs, p = 1/(R+1), exactly as the textbook says")

# --- Check 4: net R after costs --------------------------------------------
for R in (1.0, 2.0, 3.0):
    print(f"[OK] T{int(R)} gross {R:.1f}R -> net {R - cost_in_R:.4f}R")

print()
print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURES PRESENT")
