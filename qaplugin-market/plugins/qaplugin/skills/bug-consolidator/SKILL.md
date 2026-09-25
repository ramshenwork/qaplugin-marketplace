---
name: bug-consolidator
description: >
  This skill should be used when the tester hands back a completed test
  case xlsx with results marked and wants failures investigated,
  root-caused, and reported. Trigger phrases include "here are my test
  results", "these test cases failed", "consolidate these bugs", "report
  these failures to Jira".
metadata:
  version: "0.1.0"
---

# Bug Consolidator

Take the tester's marked-up test-case xlsx, root-cause every failure,
consolidate failures that share one underlying cause into a single bug,
and produce debug-ready reports. This skill writes to Jira, and every
single write — no exceptions — requires the tester's explicit confirmation
first. Never post a comment or create a ticket without showing the draft
and waiting for an explicit go-ahead.

## Input contract

The tester provides the completed xlsx (same format as
adversarial-test-writer's output) with column H and any notes on what
actually happened for each failed case. Treat every case marked failed as
a real, investigable failure — this skill does not filter for
"legitimate bug vs. bad test case." The tester already made that call by
marking it failed.

## Stage 1 — Root cause per failure

For each failed case:

1. Identify which procs/forms/nodes/screens are tied to it. Pull this
   from the stored context (`<TICKET-KEY>_context.md` from
   ticket-context-builder, and the case's own Test Data/Expected Result
   from adversarial-test-writer's output) — do not re-derive from scratch
   if it's already recorded.
2. Trace the actual mechanism of failure using nGenue-MCP trace tooling:
   `get_procedure_flow`, `get_conditional_branches`, `get_trigger_blast`,
   `get_data_flow_summary`, `trace_variable_lineage`, `get_error_handling_
   surface`, or whichever trace tool fits what actually broke. Delegate to
   `domain-knowledge-agent` for any live fact not already in context.

## Stage 2 — Connect the dots across failures

Before writing any reports, look across all failed cases for a shared
root cause. If two or more failures trace back to the same underlying
mechanism, they become **one bug**, not separate reports — even if the
symptoms looked different on the surface (e.g. one case failed on Price
Change and another on Curve Shift, but both trace to the same stale
lookup in one shared procedure). Read `references/routing-rules.md` for
the full consolidation and routing procedure before writing reports.

## Stage 3 — Write the bug report

Per consolidated bug, write:

- What failed (plain description)
- Root cause (the actual traced mechanism — proc/table/trigger names,
  the specific logic that's wrong)
- Exact reproduction steps
- Which test case IDs this bug accounts for
- Expected vs. actual behavior

Write this precisely enough that a developer could paste the description
directly into their own Claude session and start debugging immediately —
that means naming real objects and the real chain, not a vague summary
like "something is wrong with pricing."

## Stage 4 — Route, always with confirmation

Two paths, both gated the same way — draft, show the tester, wait for
explicit confirmation, only then write:

- **In-scope** (the bug traces back to this ticket's own code change):
  draft a Jira **comment** on the existing ticket. Show it to the tester.
  On confirmation, post it via the Atlassian connector.
- **Out-of-scope** (unrelated or collateral — found incidentally, not
  caused by this ticket's own change): ask the tester for every field
  needed to create the new ticket (project, issue type, priority,
  component, anything else Jira requires) — do not infer or default any
  of them. Draft the summary and description yourself, precise and
  debug-ready as above. Show the full draft to the tester. On
  confirmation, create it via the Atlassian connector.

If the tester does not confirm, or asks for changes, revise and show
again. Never proceed to the write step without an explicit yes.
