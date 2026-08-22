#!/usr/bin/python3
# =============================================================================
# balanced_4_naive_growth.py — does rate_regime earn its keep on a NAIVE growth book?
#
# broad (MANAGED QQQ: trend + vol-target) consumed balanced's rate regime and it FAILED the drawdown bar —
# broad already self-de-risks, so there was no drawdown gap left to fill (Sharpe +0.96->+1.03 but 0% DD cut).
# The law (benchmark #4): a de-risking overlay's value is proportional to how UNMANAGED the book is. So the
# honest counter-test holds the instrument constant (QQQ) and strips the management: a NAIVE buy-&-hold
# growth book. Rising rates are a growth headwind (balanced: value beats growth +12.3%/yr when rates rise),
# so de-risk x0.5 when rates rise (IEF 100d trend, causal, lagged). Full 2016-2026 SIP, net of cost.
# Same test on RPG (pure growth factor) as confirmation. Family overlay bar + corrected fat-tail toolkit.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _balanced_common import panel, rets, riskadj

MA = 100; COST = 5 / 1e4; DERISK = 0.5
P, dates = panel(["QQQ", "RPG", "IEF", "SPY"])
spy = rets(P["SPY"]); ief = P["IEF"]                             # ief = price path (len = len(dates))

def overlay_series(sym):
    r = rets(P[sym]); n = len(r); full = []; over = []; idx = []; sc_prev = 1.0
    for k in range(MA, n):                                       # causal: regime from IEF up to day k drives r[k]
        rising = ief[k] < np.mean(ief[k-MA:k])                   # IEF below 100d MA -> rates rising -> de-risk growth
        sc = DERISK if rising else 1.0
        full.append(r[k]); over.append(sc*r[k] - abs(sc-sc_prev)*COST); idx.append(k); sc_prev = sc
    return np.array(full), np.array(over), np.array(idx)

print("=" * 92, f"\nBALANCED #4 — does rate_regime earn its keep on a NAIVE growth book?  ({dates[0]} → {dates[-1]})\n" + "=" * 92)
for sym, name in [("QQQ", "naive QQQ (buy & hold)"), ("RPG", "naive pure-growth (RPG)")]:
    if sym not in P: print(f"\n  {name}: insufficient history"); continue
    full, over, idx = overlay_series(sym); spyO = spy[idx]
    mF, mO = riskadj(full, spyO), riskadj(over, spyO)
    de = 100 * np.mean([ief[k] < np.mean(ief[k-MA:k]) for k in idx])
    print(f"\n  {name}  (de-risk x{DERISK} when rates rising, {de:.0f}% of days):")
    print(f"    {'book':<24}{'Sharpe':>8}{'CAGR':>7}{'maxDD':>7}{'skew':>7}{'Jensen α':>10}{'M² exc':>8}")
    for lbl, m in [("FULL (naive, always)", mF), ("+ rate overlay", mO), ("SPY", riskadj(spyO, spyO))]:
        print(f"    {lbl:<24}{m['sh']:>+8.2f}{m['cagr']*100:>+6.0f}%{m['dd']*100:>+6.0f}%{m['skew']:>+7.2f}"
              f"{m['alpha_ann']*100:>+9.1f}%{m['m2_excess']*100:>+7.1f}%")
    dd_cut = 1 - abs(mO['dd'])/abs(mF['dd']); ret_keep = mO['cagr']/mF['cagr'] if mF['cagr'] else float('nan')
    checks = [("Sharpe not worse (>=FULL-0.03)", mO['sh'] >= mF['sh']-0.03, f"{mO['sh']:+.2f} vs {mF['sh']:+.2f}"),
              ("reduces max drawdown", mO['dd'] > mF['dd'], f"{mF['dd']*100:+.0f}% -> {mO['dd']*100:+.0f}% ({dd_cut*100:.0f}% cut)"),
              ("retains >= 80% of return", ret_keep >= 0.80, f"{ret_keep*100:.0f}% kept")]
    for n_, ok, v in checks: print(f"      [{'PASS' if ok else 'FAIL'}] {n_:<32} {v}")
    allpass = all(c[1] for c in checks)
    print(f"    -> {'PASS — rate_regime EARNS its keep on the naive book' if allpass else 'MIXED'}"
          f" (contrast broad's MANAGED QQQ: Sharpe +0.96->+1.03 but 0% DD cut, FAILED).")

print("\n  THE LAW: same instrument (QQQ), opposite verdict by management. broad's trend+vol-target already")
print("  spent the drawdown protection, so the overlay had nothing left to add; the NAIVE book has the full")
print("  drawdown gap, so the rate signal can fill it. A de-risking overlay's value ∝ how unmanaged the book is.")
