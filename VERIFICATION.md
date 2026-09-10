# Verification output

Everything below is the literal stdout of `verify_math.py` and
`sensitivity.py` in this repository. Regenerate it by running them.

## `verify_math.py`

```
-- SCENARIO ------------------------------------------
Entry 60,000.00 | Stop 58,200.00 | Distance 1,800.00
Position size : 0.05555556 units
Notional      : 3,333.33
Risk (1R)     : 100.00

-- ROUND-TRIP COSTS ----------------------------------
Commission :   3.3333
Slippage   :   0.0222
Funding    :   0.0000
TOTAL      :   3.3556
Cost as % of 1R  : 3.36 %
Break-even move  : 0.1007 %

[OK] Notional consistent (3,333.33)

-- MONTE CARLO VALIDATION OF THE WIN RATE FORMULA ----
   R   cost(R)   p required   E[R]/trade  verdict
 1.0    0.0000       50.00%      0.00144  OK
 1.0    0.0336       51.68%      0.00169  OK
 1.0    0.3000       65.00%      0.00161  OK
 2.0    0.0000       33.33%      0.00243  OK
 2.0    0.0336       34.45%      0.00259  OK
 2.0    0.3000       43.33%      0.00234  OK
 3.0    0.0000       25.00%      0.00326  OK
 3.0    0.0336       25.84%      0.00337  OK
 3.0    0.3000       32.50%      0.00333  OK

[OK] With zero costs, p = 1/(R+1), exactly as the textbook says
[OK] T1 gross 1.0R -> net 0.9664R
[OK] T2 gross 2.0R -> net 1.9664R
[OK] T3 gross 3.0R -> net 2.9664R

RESULT: ALL CHECKS PASS
```

## `sensitivity.py`

```
Round-trip cost expressed as % of 1R
(BTC/EUR, ATR=900, 2 ticks slippage per side)

   stop |    0.020%    0.050%    0.075%    0.100%    0.200%
--------+--------------------------------------------------
 0.25A |     10.8%     26.8%     40.2%     53.5%    106.8%
 0.50A |      5.4%     13.4%     20.1%     26.8%     53.4%
 1.00A |      2.7%      6.7%     10.0%     13.4%     26.7%
 1.50A |      1.8%      4.5%      6.7%      8.9%     17.8%
 2.00A |      1.4%      3.4%      5.0%      6.7%     13.4%
 3.00A |      0.9%      2.2%      3.3%      4.5%      8.9%

Win rate needed at a 2R target, by cost:
  stop 0.25xATR, commission 0.05%/side -> 33.3% in theory, 42.3% in practice (+8.9 pp)
  stop 0.25xATR, commission 0.10%/side -> 33.3% in theory, 51.2% in practice (+17.8 pp)
  stop 0.50xATR, commission 0.05%/side -> 33.3% in theory, 37.8% in practice (+4.5 pp)
  stop 0.50xATR, commission 0.10%/side -> 33.3% in theory, 42.3% in practice (+8.9 pp)
  stop 1.00xATR, commission 0.05%/side -> 33.3% in theory, 35.6% in practice (+2.2 pp)
  stop 1.00xATR, commission 0.10%/side -> 33.3% in theory, 37.8% in practice (+4.5 pp)
  stop 2.00xATR, commission 0.05%/side -> 33.3% in theory, 34.5% in practice (+1.1 pp)
  stop 2.00xATR, commission 0.10%/side -> 33.3% in theory, 35.6% in practice (+2.2 pp)

Threshold: at 0.10%/side commission, cost exceeds 30% of 1R
once the stop drops below ~0.44 x ATR  (= 396 of range in this example)
```
