#!/usr/bin/python3
# =============================================================================
# balanced_rate_emitter.py — publish the RATE regime for the Blaque Baux family.
#
# balanced's research found value is a rate-regime bet: value beats growth +12.3%/yr when rates RISE and
# lags −12.3%/yr when they FALL (one of the cleanest regime relationships in the family), though the coarse
# rotation doesn't beat the index net of cost on its own. So — exactly as bonds/brics/benchmark publish
# their regime reads even when their own trading edge is marginal — balanced's real product is the SIGNAL:
# it publishes rate_regime.txt (rising/falling rates from IEF's 100d trend) for any value-sensitive sleeve
# to consume. READ-ONLY on prices; writes only the regime file.
#
#   python3 live/balanced_rate_emitter.py            # compute + publish ~/.config/blaquebaux/rate_regime.txt
#   BB_DRYRUN=1 python3 live/balanced_rate_emitter.py  # print only, write nothing
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research"))
from _balanced_common import panel

MA = 100
OUT = os.environ.get("BB_RATE_REGIME_PATH", os.path.join(os.path.expanduser("~"), ".config", "blaquebaux", "rate_regime.txt"))

def main():
    P, dates = panel(["IEF"])
    asof = dates[-1]
    if "IEF" not in P or len(P["IEF"]) < MA + 5:
        body = f"# Blaque Baux — rate regime (published by balanced; IEF 100d trend)\nasof={asof}\nregime=unknown\nrates_rising=0\n"
        print("rate regime: unknown (insufficient IEF history)")
    else:
        ief = P["IEF"]
        ma = float(np.mean(ief[-MA:])); mom = ief[-1] / ma - 1.0
        rising = ief[-1] < ma                    # IEF below its 100d MA → duration falling → rates RISING
        tilt = "value" if rising else "growth"   # the validated implication: value↑ when rates rise
        body = ("# Blaque Baux — rate regime (published by balanced; IEF vs 100d MA)\n"
                "# research: value beats growth +12.3%/yr when rates RISE, -12.3%/yr when they FALL.\n"
                f"asof={asof}\n"
                f"ief_mom100={mom:.4f}\n"
                f"regime={'rising-rates' if rising else 'falling-rates'}\n"
                f"rates_rising={1 if rising else 0}\n"    # 1 = rates rising (tilt VALUE); 0 = falling (tilt GROWTH)
                f"value_tilt={tilt}\n")
        print(f"rate regime {asof}: IEF {mom*100:+.1f}% vs 100d MA -> "
              f"{'RISING rates (tilt VALUE)' if rising else 'FALLING rates (tilt GROWTH)'}")

    if os.environ.get("BB_DRYRUN", "") in ("1", "true", "yes"):
        print("DRYRUN — not writing.\n" + body); return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f: f.write(body)
    print(f"published -> {OUT}")

if __name__ == "__main__":
    main()
