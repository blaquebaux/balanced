#!/usr/bin/python3
# =============================================================================
# balanced_2_margin_of_safety.py — is "margin of safety" real? The tail, not the mean.
#
# Graham's claim is that cheapness is DOWNSIDE PROTECTION: you buy below intrinsic value so you're cushioned
# when wrong. That is a LEFT-TAIL claim — max drawdown, downside vol, and skew — not a return claim, and
# Sharpe alone can't judge it (JB rejects normality for equities). This sketch compares value vs growth on
# exactly those tail metrics, and asks whether the value−growth spread is a DIVERSIFIER (does value hold up
# when growth breaks?). If value's only virtue is a shallower tail, that is a legitimate — but honestly
# labeled — role, not alpha.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _balanced_common import PURE_VALUE, PURE_GROWTH, SP_VALUE, SP_GROWTH, VG_VALUE, VG_GROWTH, panel, rets, stats, jarque_bera, corr

PAIRS = [("Invesco pure", PURE_VALUE, PURE_GROWTH), ("S&P 500", SP_VALUE, SP_GROWTH), ("Vanguard", VG_VALUE, VG_GROWTH)]
def dnvol(r): r = np.asarray(r, float); d = r[r < 0]; return d.std() * np.sqrt(252) if len(d) else float('nan')

P, dates = panel([t for _, v, g in PAIRS for t in (v, g)] + ["SPY"])
print("=" * 92, f"\nBALANCED #2 — margin of safety = the left tail  ({dates[0]} → {dates[-1]})\n" + "=" * 92)
print(f"  {'pair / side':<22}{'maxDD':>8}{'downside vol':>14}{'skew':>8}{'exkurt':>8}   safer tail?")
for label, v, g in PAIRS:
    if v not in P or g not in P: print(f"  {label:<22}  (insufficient history)"); continue
    rv, rg = rets(P[v]), rets(P[g])
    sv, sg = stats(rv), stats(rg); jv, jg = jarque_bera(rv), jarque_bera(rg)
    safer = (sv['dd'] > sg['dd']) and (dnvol(rv) < dnvol(rg))     # shallower DD AND lower downside vol
    print(f"  {label+' VALUE':<22}{sv['dd']*100:>+7.0f}%{dnvol(rv)*100:>13.1f}%{jv['skew']:>+8.2f}{jv['exkurt']:>8.1f}"
          f"   {'← value safer' if safer else ''}")
    print(f"  {label+' growth':<22}{sg['dd']*100:>+7.0f}%{dnvol(rg)*100:>13.1f}%{jg['skew']:>+8.2f}{jg['exkurt']:>8.1f}")

# does value diversify a growth crash? correlation + crash-day behavior
rv, rg = rets(P[PURE_VALUE]), rets(P[PURE_GROWTH])
gcrash = rg < np.percentile(rg, 5)                                 # worst-5% growth days
print(f"\n  Diversification test (Invesco pure): corr(value,growth) {corr(rv, rg):+.2f}")
print(f"    on growth's worst-5% days: growth avg {rg[gcrash].mean()*100:+.2f}%/day, value avg {rv[gcrash].mean()*100:+.2f}%/day"
      f"  → value {'CUSHIONS' if rv[gcrash].mean() > rg[gcrash].mean() else 'falls with'} the growth crash")
print("\n  READ: if value shows a shallower drawdown / lower downside vol / less-negative skew, the")
print("  margin-of-safety claim holds as TAIL protection — a real role even where value lags on return.")
