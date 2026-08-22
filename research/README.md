# Blaque Baux Balanced — research

Is value investing still an edge — and is "margin of safety" real? The value factor isolated (Invesco pure
`RPV`/`RPG`, S&P `IVE`/`IVW`, Vanguard `VTV`/`VUG`) vs `SPY`, on return, on the *left tail*, and conditioned
on the rate regime (`IEF` trend). Read-only Alpaca SIP bars, 2016–2026. Verdicts use the family fat-tail
toolkit ([`_balanced_common.py`](_balanced_common.py): Jarque-Bera + Jensen's alpha + M², Sharpe-difference
form so the benchmark vs itself = 0).

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
python research/balanced_1_value_vs_growth.py   # risk-adjusted value vs growth
python research/balanced_2_margin_of_safety.py  # is cheapness a shallower tail? (the safety claim)
python research/balanced_3_regime.py            # is value a conditional keeper (rising rates)?
```

## Scorecard (2016-01 → 2026-07 SIP, vs SPY)

| # | Question | Result | Verdict |
|---|----------|--------|---------|
| 1 | Does value earn a risk-adjusted premium? | value LAGS growth: RPV Sharpe +0.60 / α −2.3% / M² −4.9% vs RPG +0.66 / −3.4% / −3.9%; value−growth spread **−1.9%/yr**, corr **+0.68** | ❌ a lower/different **beta**, not alpha (this decade) |
| 2 | Is "margin of safety" real (shallower tail)? | **0/3 pairs** safer on the strict test: pure value's **maxDD −51% vs growth −37%**, skew **−0.59 vs −0.21**, fatter kurtosis. Value's *only* safety: lower **downside vol** (13.6% vs 16.8%) and it **cushions growth-specific crashes** (−2.1%/day vs −3.5% on growth's worst days) | ⚠️ **mostly a myth** — value crashes *harder* (2020 cyclicals); "safety" is diversification, not absolute downside |
| 3 | Is value a *conditional* keeper (rising rates)? | **strikingly symmetric**: value−growth **+12.3%/yr when rates rise, −12.3%/yr when they fall**. Rate-timed rotation Sharpe +0.86 / α +1.8% / **M² −0.5%** — beats static value & growth, ~matches but **doesn't clear** SPY | ✅ **clearly regime-conditional**, but the coarse timing doesn't beat the index net of cost |

## The synthesis

**"Is value still crucial to safety?" — the honest answer is: not the way the folklore says.** Three passes:

1. **Value lagged growth risk-adjusted this decade — a different beta, not alpha.** Across all three
   definitions growth edged value on Sharpe and M²; the pure value−growth spread ran −1.9%/yr, and at 0.68
   correlation the two aren't even good diversifiers of each other. Consistent with
   [bogle](https://github.com/blaquebaux/bogle): style tilts don't beat the cap-weighted index risk-adjusted.
2. **The "margin of safety" is largely a myth in this sample — value crashed *harder*.** The folklore says
   cheapness cushions the downside; the tail says otherwise. Pure value's max drawdown was **−51% vs growth's
   −37%**, with a more negative skew (−0.59) and fatter kurtosis — because deep value loads on cyclicals /
   financials / energy that were hit hardest in the 2020 COVID crash. Value's *genuine* virtues are narrower:
   lower day-to-day **downside volatility**, and it **cushions a growth-led selloff** (a diversification role).
   So "safety" is real only as *diversification against growth-specific risk*, not as absolute downside protection.
3. **Value's real signal is the rate regime — and it's strong, but not a standalone keeper.** Value beats
   growth by **+12.3%/yr when rates rise** and loses by the same when they fall — one of the cleanest,
   most symmetric regime relationships in the family. A rate-timed value/growth rotation beats both static
   styles and nearly matches SPY, but a coarse 100-day rate trend **doesn't clear the index hurdle net of
   cost** (M² −0.5%). The signal is real; the timing is too blunt to monetize alone — a classic
   **conditional-keeper ingredient**, not a standalone edge.

**Margin of safety belongs at the security level, not the factor level.** As a *factor*, "value" this decade
was lower-vol-with-worse-crashes and a rate bet in disguise — not the safe-haven premium of legend. The
Graham idea (buy below intrinsic value) is a *bottom-up* discipline the top-down value ETF can't capture.

## Status
**Research: first pass complete — value is a rate-regime bet, and "margin of safety" is mostly a myth at the
factor level.** Value lagged growth risk-adjusted (a different beta), crashed *harder* than growth (−51% vs
−37% — the safety folklore inverted), and its one strong, clean signal is rate-conditional (+12/−12%/yr) but
too coarse to beat the index net of cost. A conditional-keeper ingredient, not a standalone edge. No live driver.
