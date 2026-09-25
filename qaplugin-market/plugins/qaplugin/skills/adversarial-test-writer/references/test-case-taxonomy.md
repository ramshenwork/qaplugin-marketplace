# Adversarial Test Case Taxonomy

Seven categories. Work through all of them for every relevant entity —
do not skip a category because it seems less likely to find something;
the whole point of this skill is to not pre-judge which angle breaks it.

## 1. Positive

Every valid variant, not just the one obvious happy path. If the domain
has multiple valid deal types, gas types, pricing types, or retail/
wholesale flow variants that touch the changed entity, write one case per
valid combination that's actually relevant to the change — not an
exhaustive cross-product of unrelated variants.

## 2. Negative

Invalid input, wrong permission level for the action, wrong workflow
state for the action to be legal. Use nGenue-MCP to confirm what actually
constitutes "invalid" here (a real constraint, a real permission constant)
rather than assuming.

## 3. Boundary / Edge

Min/max values, empty/null, zero, exact threshold crossings, off-by-one
on any limit the form or procedure enforces. If the domain-knowledge-agent
confirms a real numeric or date boundary, test one value inside it, the
value exactly at it, and one value just past it.

## 4. State & Sequence

Doing steps out of order, skipping a required prior step, repeating the
same action twice, closing/reopening mid-flow, performing the action from
a state it wasn't designed to be performed from.

## 5. Regression

See SKILL.md's special handling. Reconstruct the exact prior bug
condition from context.md's Prior Bugs section, then write cases probing
adjacent paths to that condition — not just the literal reported case.

## 6. Blast-radius / Collateral

Cases that don't touch the changed object directly but touch something
context.md's Unaware-Mode Findings flagged as dependent — another form
bound to the same table, a trigger that fires downstream, a proc that
calls the changed one. The point is to catch damage the ticket's author
never considered because it's outside their own change.

## 7. Concurrency / Data-integrity

Only where the domain plausibly applies (e.g. two users hitting the same
deal/record at once, a trigger firing while a batch process like PLEX
runs). Do not force this category where it doesn't apply — an irrelevant
concurrency case adds noise, not coverage.

## Worked example

Ticket: adds a new "Curve Shift" recalculation path for Futures deals
after a Base Index configuration change (Unaware entity — new logic).

- Positive: Curve Shift reflects a base index curve movement for a
  standard Futures deal after normal Base Index config.
- Negative: attempt to trigger Curve Shift recalculation with no Base
  Index configured for the Exchange at all.
- Boundary: Base Index configuration changed on the exact day of a PLEX
  run vs. the day before vs. the day after.
- State & Sequence: change the Base Index, then immediately cancel the
  deal before the next PLEX run — does Curve Shift still fire, or does
  cancellation correctly suppress it?
- Regression: if a prior bug involved Curve Shift using a stale hardcoded
  index (see context.md Prior Bugs), test a second Exchange with a
  different Base Index to confirm the fix wasn't specific to the one
  Exchange originally reported.
- Blast-radius: if Unaware-Mode Findings shows another form reads from
  the same curve table, verify that form still shows correct values after
  this change, even though the ticket never mentions that form.
- Concurrency: two PLEX runs triggered back-to-back before the first
  completes, with a Base Index change landing in between.

Every one of those seven is a distinct row in the output xlsx, written to
the exact column structure in SKILL.md Stage 4.
