# Consolidation & Routing — Full Procedure

## Consolidation: when do two failures become one bug?

Two failed cases collapse into a single bug report when their traced root
causes point to the same underlying mechanism — the same procedure logic,
the same trigger, the same bad lookup, the same missing validation — even
if the surface symptom differs.

Do not consolidate on symptom similarity alone (two cases that both show
"wrong dollar amount" are not automatically the same bug — trace first,
then compare root causes, not descriptions).

Do not force consolidation to reduce report count. If two failures trace
to genuinely different mechanisms, they stay as two separate bug reports
even if they're on the same ticket or the same screen.

Worked example:

- TC 019 (Swap price change) fails: Price Change column shows an
  incorrect value.
- TC 027 (Futures price change) fails: Price Change column shows an
  incorrect value.
- Trace: both call into the same shared pricing-delta procedure, and both
  hit the same conditional branch that uses the wrong prior-value lookup.
- Result: **one bug** — "shared pricing-delta procedure uses stale prior
  value for both Swap and Futures price changes" — referencing both
  TC 019 and TC 027, not two separate reports.

## Routing: in-scope vs. out-of-scope

**In-scope** — the traced root cause sits inside the code change this
ticket was actually for. Check context.md's ticket description and the
Aware/Unaware entity list: if the failing mechanism is the entity the
ticket set out to change, it's in-scope.

**Out-of-scope** — the traced root cause is collateral: it sits in code
the ticket never touched, surfaced only because testing this ticket
happened to exercise it (a pre-existing issue, a different area entirely,
something flagged under Unaware-mode blast-radius that turned out to
already be broken independent of this ticket's change).

If genuinely ambiguous after tracing, state the ambiguity explicitly to
the tester when presenting the draft rather than picking a side silently
— let the tester make the final call along with their confirmation.

## What "explicit confirmation" means in practice

Present the full draft (comment text, or ticket summary + description +
whatever fields were gathered) verbatim to the tester and ask directly:
post this / create this — yes or no. A tester's general approval of the
bug findings earlier in the conversation is not confirmation of the
specific write. Each write gets its own explicit yes, every time.
