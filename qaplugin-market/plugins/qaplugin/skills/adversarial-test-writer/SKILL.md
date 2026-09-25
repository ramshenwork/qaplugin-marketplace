---
name: adversarial-test-writer
description: >
  This skill should be used when the tester wants test cases written for
  a ticket that already has a context file built by ticket-context-builder,
  or asks to write test cases, break-it cases, or QA cases for a ticket.
  Trigger phrases include "write test cases for TICKET-123", "generate
  test cases", "give me every test case you can think of for this ticket".
metadata:
  version: "0.1.0"
---

# Adversarial Test Writer

Write exhaustive test cases whose purpose is to break the change under
test, not confirm it works. This skill produces an xlsx in a fixed format
that must match the tester's reference sample exactly — never improvise
the format.

## Preconditions

Requires `<TICKET-KEY>_context.md` from ticket-context-builder to already
exist in the sandbox. If it doesn't exist, tell the tester and offer to
run ticket-context-builder first rather than guessing at context.

## Mandate

The goal of every test case is to find where the change fails, not to
demonstrate it works. Read `references/test-case-taxonomy.md` before
generating cases — it defines the seven categories to cover and gives
worked examples of the adversarial mindset per category. Do not skip
categories. Do not cap volume or prioritize a subset — write every case
you can reason out; this skill is deliberately uncapped.

## Stage 1 — Read context

Read the full `<TICKET-KEY>_context.md`, especially the Consolidated
Knowledge Summary, the Per-Entity Classification, and both Aware-Mode and
Unaware-Mode Findings sections. Every test case must trace back to
something in this file — the ticket's own change, or an entity flagged in
Unaware-mode blast-radius.

## Stage 2 — Pull live facts as needed

The stored context file will not contain every fact needed to write a
precise boundary or negative case (e.g. the actual valid range on a field,
an actual FK constraint, an actual permission constant). When a case needs
a fact the context file doesn't have, delegate to the
`domain-knowledge-agent` sub-agent rather than guessing or inventing a
plausible-sounding value. A test case built on an invented constraint is
worse than useless — it will fail for the wrong reason.

## Stage 3 — Generate cases across all seven categories

For every relevant entity in context.md, work through: Positive,
Negative, Boundary/Edge, State & Sequence, Regression, Blast-radius /
Collateral, and Concurrency/Data-integrity (where the domain applies).
Full detail and worked examples for each category are in
`references/test-case-taxonomy.md`.

**Regression cases get special treatment.** If context.md's Prior Bugs
section shows a bug was closed on this ticket or a related one,
reconstruct the exact broken condition that caused it, then write cases
that approach that condition from adjacent angles — not just "verify the
bug doesn't recur," but cases that probe whether the fix only handles the
exact reported path while leaving a sibling path open to the same failure.

**Two special row types**, matching the tester's own established
convention:

- **Instruction row** — for a case that identifies a real caution or an
  unsaid rule the tester must follow, but that the system itself does not
  and cannot validate (e.g. "the system won't block this state change, so
  don't perform it"). Description starts with `Instruction:`. Not a real
  executable test — no Pass/Fail expected.
- **Future Scope row** — for a genuine gap: something this skill cannot
  test with confidence right now, typically because an Unaware-mode entity
  has no reliable baseline yet, or a dependency is confirmed not built.
  Description starts with `[Future Scope]`. Fill Pre-Condition, Test
  Steps, Test Data and Expected Result as best-effort/best-known. Leave
  column H blank, matching the reference sample's own treatment.

## Stage 4 — Build the xlsx

Do not construct the xlsx by hand-writing cell formatting. Assemble the
full case list as a JSON array (schema documented in the script's
docstring) and run:

```
python3 scripts/build_test_case_xlsx.py <output_path> <cases.json>
```

This produces a workbook with the exact header fill, font, column widths,
wrap/valign, and row height as the tester's reference sample. Column H is
always left blank on output — it is the tester's field to fill in after
actually executing the cases against the application.

Save the output file, present it to the tester, and state the case count
per category. Do not proceed to bug-consolidator work in the same run —
that only happens once the tester hands the file back with results
marked.
