# Blaque Baux Balanced — research

Is value investing still an edge — and is it regime-conditional? The value factor, isolated (pure
value/growth `RPV`/`RPG`, plus `IVE`/`IVW`, `VTV`/`VUG`) vs `SPY`, conditioned on the rate regime
(`IEF`/`SHY`). Read-only Alpaca SIP bars. Because "margin of safety" is a left-tail claim, verdicts pair
drawdown + Jarque-Bera with Jensen's alpha and M² ([`_balanced_common.py`](_balanced_common.py)).

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
# python research/balanced_1_value_vs_growth.py  # [to build] RPV vs RPG: Jensen α, M², JB, maxDD
# python research/balanced_2_margin_of_safety.py  # [to build] does cheapness cushion the left tail?
# python research/balanced_3_regime.py            # [to build] value vs growth conditioned on the rate regime
```

## Planned scorecard

| # | Question | Metric | Status |
|---|----------|--------|--------|
| 1 | Does value earn a risk-adjusted premium? | Jensen's α, M², JB vs growth | ☐ to build |
| 2 | Is "margin of safety" real (shallower left tail)? | maxDD, downside vol | ☐ to build |
| 3 | Is value a *conditional* keeper (rising rates)? | value−growth vs `IEF` trend | ☐ to build |

**The prior:** value is regime-conditional — a lost decade under falling rates, a comeback in 2022 — so
likely a conditional keeper, with "safety" (tail cushion) as much the product as alpha.

## Status
**[Concept] — plan defined, no sketches run.** Clean ETF data path set. Next: sketches #1–#3.
