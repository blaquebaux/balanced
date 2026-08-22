#!/usr/bin/python3
# =============================================================================
# balanced_3_regime.py — is value a CONDITIONAL keeper? Value vs growth by the rate regime.
#
# Value's fortunes swing with rates: it won when rates rose (2022), lost through the zero-rate 2010s. So the
# honest question isn't "is value good?" but "is value good WHEN rates rise?" — a conditional-keeper test.
# Causal, lagged rate regime from IEF's 100d trend (IEF below its MA = duration falling = rates rising),
# applied to next-day returns. Compares the value−growth spread across regimes and a regime-timed style
# rotation (hold value when rates rise, growth when they fall) vs plain SPY, net of switching cost.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _balanced_common import PURE_VALUE, PURE_GROWTH, panel, rets, riskadj, stats

MA = 100; COST = 5 / 1e4
P, dates = panel([PURE_VALUE, PURE_GROWTH, "IEF", "SPY"])
rv, rg, spy = rets(P[PURE_VALUE]), rets(P[PURE_GROWTH]), rets(P["SPY"])
ief = P["IEF"]                                                    # price path, len T+1 (returns are T)
rising = np.zeros(len(rv), bool)                                  # causal: signal at day t uses IEF up to t
for t in range(MA, len(rv)): rising[t] = ief[t] < ief[t-MA:t].mean()   # IEF below MA → rates rising

vmg = rv - rg
print("=" * 90, f"\nBALANCED #3 — is value a CONDITIONAL keeper (rising rates)?  ({dates[0]} → {dates[-1]})\n" + "=" * 90)
print(f"  rate regime from IEF 100d trend — rates RISING {100*rising.mean():.0f}% of days\n")
def ann(x): return (1 + np.mean(x))**252 - 1
print(f"  value−growth (RPV−RPG) spread:")
print(f"    rising-rate days : {ann(vmg[rising])*100:+6.1f}%/yr   (value {'BEATS' if vmg[rising].mean()>0 else 'lags'} growth)")
print(f"    falling-rate days: {ann(vmg[~rising])*100:+6.1f}%/yr   (value {'beats' if vmg[~rising].mean()>0 else 'LAGS'} growth)")

# regime-timed style rotation: value when rising, growth when falling (causal, lagged), net of switching cost
pos_val = np.roll(rising, 1); pos_val[0] = False                 # yesterday's signal drives today
rot = np.where(pos_val, rv, rg).astype(float)
switch = np.abs(np.diff(np.concatenate([[0.0], pos_val.astype(float)])))
rot = rot - switch * COST
print(f"\n  {'book':<34}{'Sharpe':>8}{'CAGR':>7}{'maxDD':>7}{'Jensen α':>10}{'M² exc':>8}")
for lbl, r in [("regime rotation (val↑rates/grow↓)", rot), ("static value (RPV)", rv),
               ("static growth (RPG)", rg), ("SPY (hurdle)", spy)]:
    m = riskadj(r, spy)
    print(f"  {lbl:<34}{m['sh']:>+8.2f}{m['cagr']*100:>+6.0f}%{m['dd']*100:>+6.0f}%{m['alpha_ann']*100:>+9.1f}%{m['m2_excess']*100:>+7.1f}%")

mrot = riskadj(rot, spy)
print(f"\n  VERDICT: value is {'CLEARLY regime-conditional' if vmg[rising].mean()>0 and vmg[~rising].mean()<0 else 'only weakly regime-conditional'} "
      f"(value beats growth when rates rise, lags when they fall).")
print(f"  The regime rotation {'BEATS' if mrot['alpha_ann']>0 and mrot['m2_excess']>0 else 'does NOT beat'} the SPY hurdle risk-adjusted "
      f"(Jensen α {mrot['alpha_ann']*100:+.1f}%, M² {mrot['m2_excess']*100:+.1f}%) — "
      f"{'a conditional keeper' if mrot['alpha_ann']>0 and mrot['m2_excess']>0 else 'the timing is real but too coarse to clear the index net of cost'}.")
