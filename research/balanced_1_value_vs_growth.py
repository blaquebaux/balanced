#!/usr/bin/python3
# =============================================================================
# balanced_1_value_vs_growth.py — does VALUE earn a risk-adjusted premium, or just a different beta?
#
# The value factor across three definitions — Invesco PURE value/growth (RPV/RPG, blend stripped), S&P
# (IVE/IVW), Vanguard (VTV/VUG) — each vs SPY with the family fat-tail toolkit. The honest number is
# Jensen's ALPHA (return beyond SPY's beta) and M² (risk-adjusted to SPY's vol, benchmark-vs-itself = 0).
# Over a growth-led 2016-2026, the prior is that value LAGS on return; the question is whether it lags
# risk-adjusted too, or whether it's simply a lower-beta slice of the same market.
# =============================================================================
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _balanced_common import FACTOR, PURE_VALUE, PURE_GROWTH, panel, rets, riskadj, corr

P, dates = panel(FACTOR + ["SPY"])
spy = rets(P["SPY"])
print("=" * 92, f"\nBALANCED #1 — value vs growth, risk-adjusted  ({dates[0]} → {dates[-1]}, {len(dates)} days)\n" + "=" * 92)
print(f"  {'fund':<20}{'Sharpe':>8}{'CAGR':>7}{'maxDD':>7}{'beta':>6}{'Jensen α':>10}{'M² exc':>8}{'skew':>7}{'JB p':>7}")
for s in FACTOR:
    if s not in P: print(f"  {s:<20}  (insufficient history)"); continue
    m = riskadj(rets(P[s]), spy)
    style = "value" if s in (PURE_VALUE, "IVE", "VTV") else "growth"
    print(f"  {s+' ('+style+')':<20}{m['sh']:>+8.2f}{m['cagr']*100:>+6.0f}%{m['dd']*100:>+6.0f}%{m['beta']:>6.2f}"
          f"{m['alpha_ann']*100:>+9.1f}%{m['m2_excess']*100:>+7.1f}%{m['skew']:>+7.2f}{m['p']:>7.3f}")

# the pure value-minus-growth long/short factor
rv, rg = rets(P[PURE_VALUE]), rets(P[PURE_GROWTH])
vmg = rv - rg
mv, mg = riskadj(rv, spy), riskadj(rg, spy)
print(f"\n  PURE value vs growth (RPV−RPG):")
print(f"    value  Jensen α {mv['alpha_ann']*100:+.1f}%  M² {mv['m2_excess']*100:+.1f}%   |   "
      f"growth Jensen α {mg['alpha_ann']*100:+.1f}%  M² {mg['m2_excess']*100:+.1f}%")
print(f"    value−growth spread: CAGR {( (1+vmg.mean())**252-1 )*100:+.1f}%/yr, corr(value,growth) {corr(rv, rg):+.2f}")
verdict = ("VALUE earns a risk-adjusted premium" if mv['m2_excess'] > mg['m2_excess'] and mv['alpha_ann'] > 0
           else "value LAGS growth risk-adjusted this decade — a different (lower) beta, not alpha")
print(f"\n  VERDICT: {verdict}. (Return is only half the question — sketch #2 tests the margin-of-safety/tail claim.)")
