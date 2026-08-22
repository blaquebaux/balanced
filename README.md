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

## Status
**[Concept] — scaffolded, not yet built.** Thesis (margin of safety; value-vs-growth as factor, distinct
from the buffett blend), the conditional-keeper angle (value ~ rising rates), and the clean ETF data path
are defined. Verdicts use the fat-tail toolkit (Jarque-Bera + Jensen's alpha + M²). No research run yet; no
live driver.

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
research/   _balanced_common.py (loaders + JB/Jensen/M² toolkit) + sketches + scorecard  [to build]
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
