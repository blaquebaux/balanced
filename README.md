# Blaque Baux Balanced

**Margin of safety — is value investing still a real edge, or a lost decade?**

Balanced is a member of the Blaque Baux family. The [core repo](https://github.com/blaquebaux/base)
is the **engine and blueprint** — a governed, systematic platform (Julia) with a venue-agnostic
execution controller and a Layer-3 live-money safety gate. Balanced points that engine at the oldest
question in the book — does cheap beat dear? — and inherits the governance wholesale.

> **Not investment advice.** Educational/research software. Nothing here is validated. See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/blaquebaux/balanced.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

Graham's *margin of safety* — buy below intrinsic value so you're protected when you're wrong — is the
foundation of value investing. But value spent the 2010s **losing to growth** (the "value is dead" decade),
then roared back in the 2022 rate shock. So the honest question isn't "is value good?" but "is value **still
crucial to safety**, and *when*?" This is the **value factor** (cheap vs expensive), distinct from the
[buffett](https://github.com/blaquebaux/buffett) sleeve's cheap-safe-quality *blend* — here we isolate value
vs growth itself, and ask whether it's an unconditional edge or a **regime-conditional** one (a natural
[conditional-keeper](https://github.com/blaquebaux/benchmark) case: value tends to win when rates rise).

**Data honesty — clean, ETF-based.** The value/growth factor is directly priceable: `IVE`/`IVW` (S&P
value/growth), `VTV`/`VUG` (Vanguard), and the *pure* factor `RPV`/`RPG` (Invesco pure value/growth) which
strip the blend. Rates via `IEF`/`SHY`. No private data; the only limit is that ETF factor definitions are
coarse vs a true fundamental cheapness screen — flagged.

## Research plan (Path A)

- **Value vs growth, risk-adjusted.** `RPV` vs `RPG` (and `IVE`/`IVW`) over the full cycle: Jensen's alpha,
  M², Jarque-Bera, drawdown — does value earn a *risk-adjusted* premium, or just a different beta?
- **The margin-of-safety test.** Does value's cheapness cushion drawdowns (shallower left tail) even when
  it lags on return — i.e. is "safety" the real product rather than alpha?
- **Regime-conditional value.** Value vs growth conditioned on the rate regime (`IEF` trend): is value a
  *conditional* keeper — on when rates rise, off when they fall?

## Research — first pass done

Full detail in [`research/README.md`](research/README.md). Scorecard (Alpaca SIP, 2016–2026, vs `SPY`):

| # | Question | Verdict |
|---|----------|---------|
| 1 | Does value earn a risk-adjusted premium? | ❌ value **lags growth** — a lower/different beta, not alpha (RPV α −2.3% / M² −4.9% vs RPG −3.4% / −3.9%; spread −1.9%/yr, corr +0.68) |
| 2 | Is "margin of safety" real (shallower tail)? | ⚠️ **mostly a myth** — pure value's **maxDD −51% vs growth −37%**, worse skew (−0.59); value crashed *harder* (2020 cyclicals). Its only safety: lower downside vol + cushioning growth-specific selloffs (diversification, not absolute downside) |
| 3 | Is value a *conditional* keeper (rising rates)? | ✅ **clearly regime-conditional** — value−growth **+12.3%/yr rising rates, −12.3%/yr falling**; but a rate-timed rotation (α +1.8% / M² −0.5%) beats both styles yet **doesn't clear** the SPY hurdle net of cost |
| 4 | Does the published signal earn its keep on a **naive** growth book? | ✅ **naive QQQ PASS 3/3** — DD −35%→−29% (18% cut), Sharpe +0.95→+1.04, keeps 90% (managed broad's QQQ failed — it self-manages). The overlay earns it where the book is unmanaged *and* its worst DD is rate-driven |

**The synthesis:** *"Is value still crucial to safety?"* — not the way the folklore says. As a **factor** this
decade, value was a lower-vol-with-worse-crashes **rate bet in disguise**: it lagged growth risk-adjusted,
crashed *harder* than growth (−51% vs −37% — the margin-of-safety claim inverted), and its one clean, strong
signal is rate-conditional (+12/−12%/yr) but too coarse to beat the index net of cost. A conditional-keeper
**ingredient**, not a standalone edge. Margin of safety belongs at the **security** level (Graham's bottom-up
discipline), not the top-down value ETF — which is exactly what separates this from the
[buffett](https://github.com/blaquebaux/buffett) blend and the [bogle](https://github.com/blaquebaux/bogle) hurdle.

## Status
**Research: first pass complete — value is a rate-regime bet, "margin of safety" mostly a myth at the factor
level.** Value lagged growth risk-adjusted, crashed harder than growth (−51% vs −37%), and its strong clean
signal is rate-conditional (+12/−12%/yr) but too coarse to beat the index net of cost. A conditional-keeper
ingredient, not a standalone edge. No trading driver — it publishes its signal for the family (below).

## Live — publishes the rate regime (`rate_regime.txt`)

The rotation isn't a standalone keeper, but the *signal underneath it* is clean and strong — so, exactly as
[bonds](https://github.com/blaquebaux/bonds)/[brics](https://github.com/blaquebaux/brics)/[benchmark](https://github.com/blaquebaux/benchmark)
publish their regime reads even when their own trading edge is marginal, **balanced publishes the rate
regime** as its real product. [`live/balanced_rate_emitter.py`](live/balanced_rate_emitter.py) writes
`~/.config/blaquebaux/rate_regime.txt` — the rising/falling-rate state from `IEF`'s 100d trend, with the
validated implication (`value_tilt=value` when rates rise, `growth` when they fall). Any value-sensitive
sleeve can consume it; read-only on prices, it writes only the regime file.

```bash
python3 live/balanced_rate_emitter.py           # publish ~/.config/blaquebaux/rate_regime.txt
BB_DRYRUN=1 python3 live/balanced_rate_emitter.py   # print only, write nothing
```

The published signal is the family's 4th regime read (alongside bonds' stock-bond correlation, brics'
dollar trend, and benchmark's market internals). Honestly labeled: the regime is real; the coarse rotation
it drives doesn't beat the index alone — it's an *ingredient* for a consumer to combine.

**The signal is validated to earn its keep — on the right consumer.**
[`research/balanced_4_naive_growth.py`](research/balanced_4_naive_growth.py) tests it on a **naive** growth
book: de-risking buy-&-hold **QQQ** when rates rise **passes the full family bar** (DD −35%→−29%, a 18% cut;
Sharpe +0.95→+1.04; keeps 90% of return). The *same* signal on *managed* QQQ ([broad](https://github.com/blaquebaux/broad),
trend + vol-target) cut 0% off drawdown and shipped opt-in — because broad already spent the drawdown
protection. The law (benchmark #4): **a de-risking overlay's value ∝ how unmanaged the book is** — and here,
also whether the book's worst drawdown is actually rate-driven (QQQ's was 2022; RPG's was 2020, so RPG is mixed).

## About Blaque Baux

**Blaque Baux** is a quantitative research initiative and a subsidiary of **[Carter Warrens](https://carterwarrens.com)**.
[**BlaqueBaux.com**](https://blaquebaux.com) is the home for the work; the code lives here on GitHub — open to
study, test, and build bespoke strategies on top of.

Anyone can point an AI at a market. The edge is **understanding what the data actually says — and turning it
into something you can act on.** We test relentlessly and put most of it *on the record as rejected, with the
reason*; what survives is built, governed, and validated before it is ever called real. That combination —
honest research, reproducible evidence, and execution you can trust — is why Carter Warrens leads on
**strategy and implementation**, not merely uses the tools everyone now has.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/blaquebaux/base) is the
base/blueprint and holds the [full family roster](https://github.com/blaquebaux/base#the-blaquebaux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> blaquebaux/base)
research/   _balanced_common.py (loaders + JB/Jensen/M² toolkit) + balanced_1_value_vs_growth / _2_margin_of_safety / _3_regime / _4_naive_growth + scorecard
live/       balanced_rate_emitter.py (publishes rate_regime.txt) + run_balanced_rate.sh + plist
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
