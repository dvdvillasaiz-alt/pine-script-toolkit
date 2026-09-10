"""
Where trading costs kill a strategy: sensitivity of the cost drag to stop
distance and commission. These are the numbers quoted in the README, so this
script is what makes them checkable rather than merely asserted.

Run with:  python3 sensitivity.py
"""
entry, atr, mintick, slip_ticks = 60_000.0, 900.0, 0.1, 2

def drag(atr_mult, comm_pct, risk_amt=100.0):
    """Round-trip cost as a fraction of 1R."""
    stop_dist = atr * atr_mult
    pos   = risk_amt / stop_dist
    noti  = pos * entry
    total = noti * comm_pct/100*2 + pos*slip_ticks*mintick*2
    return total / risk_amt

print("Round-trip cost expressed as % of 1R")
print("(BTC/EUR, ATR=900, 2 ticks slippage per side)\n")
mults = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0]
combs = [0.02, 0.05, 0.075, 0.10, 0.20]
print(f"{'stop':>7} |" + "".join(f"{c:>9.3f}%" for c in combs))
print("-"*7 + "-+" + "-"*(10*len(combs)))
for m in mults:
    row = f"{m:>5.2f}A |"
    for c in combs:
        row += f"{drag(m, c)*100:>9.1f}%"
    print(row)

print("\nWin rate needed at a 2R target, by cost:")
for m in [0.25, 0.5, 1.0, 2.0]:
    for c in [0.05, 0.10]:
        d = drag(m, c)
        p_free = 1/(2+1)
        p_real = (1+d)/(2+1)
        print(f"  stop {m:>4.2f}xATR, commission {c:.2f}%/side -> "
              f"{p_free*100:.1f}% in theory, {p_real*100:.1f}% in practice "
              f"(+{(p_real-p_free)*100:.1f} pp)")

print("\nThreshold: at 0.10%/side commission, cost exceeds 30% of 1R")
print("once the stop drops below ~", end="")
m = 3.0
while drag(m, 0.10) < 0.30 and m > 0.01:
    m -= 0.01
print(f"{m:.2f} x ATR  (= {atr*m:,.0f} of range in this example)")
