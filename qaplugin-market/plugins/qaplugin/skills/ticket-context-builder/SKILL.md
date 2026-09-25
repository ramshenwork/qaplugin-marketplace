---
name: ticket-context-builder
description: >
  This skill should be used when the tester names a Jira ticket key and
  wants full ticket and nGenue application context gathered before test
  cases can be written. Trigger phrases include "pull context for
  TICKET-123", "build context for this ticket", "get me the domain
  knowledge for TICKET-123", "gather everything on TICKET-123", or any
  request to understand a ticket's full background before testing it.
metadata:
  version: "0.1.0"
---

# Ticket Context Builder

Build a single, structured knowledge file per ticket that later skills
(adversarial-test-writer, bug-consolidator) read as their primary input.
This skill is read-only — it never writes to Jira or anywhere outside the
sandbox.

## When to run

Run whenever the tester names a ticket key and no `<TICKET-KEY>_context.md`
already exists in the sandbox for this chat, or when the tester explicitly
asks to rebuild/refresh context for a ticket already processed.

## Stage 1 — Pull Jira knowledge

Using the Atlassian connector, gather for the named ticket:

1. Full ticket details: summary, description, status, issue type, all
   custom fields, acceptance criteria if present.
2. Ticket history / changelog: every status transition, who made it, when.
3. Related tickets: linked issues (blocks / is blocked by / relates to),
   sub-tasks, parent epic and sibling tickets under that epic.
4. Prior bugs: any bug-type tickets raised against this ticket specifically
   and their resolution — what was reported, what was the root cause, how
   it was fixed, and whether it is currently closed or reopened.

Do not summarize or drop detail at this stage. This is the raw material
Stage 2 and later skills reason over — capture it completely.

## Stage 2 — Identify domain entities in the Jira knowledge

Read through everything pulled in Stage 1 and extract every concrete
nGenue domain noun mentioned or implied:

- Screen / form names (Delphi forms, data modules, frames)
- SQL objects: stored procedures, functions, triggers, tables, views
- Business-process references: retail vs wholesale flow, deal type
  (Physical, Swap, Futures, etc.), gas type, tier/month structure,
  pricing type (Fixed, Index)
- Anything else that names a specific piece of the nGenue application
  rather than a general software concept

Build a candidate list. Do not filter yet — over-collect here, since a
missed entity means a blind spot in the domain knowledge later skills
depend on.

## Stage 3 — Classify each entity: Aware or Unaware

This classification happens **per entity, not per ticket**. A single
ticket routinely produces a mix of Aware and Unaware entities.

For each candidate entity, query nGenue-MCP (`find_form_by_name`,
`find_procedure_by_name`, `find_table_by_name`,
`search_sql_objects_by_name`, `get_object_description`, or the closest
matching lookup tool for that entity type).

- If nGenue-MCP returns a match, **do not accept it on name similarity
  alone.** Cross-reference the returned object's actual description,
  fields, or behavior against what the Jira context says this entity is
  for. Only classify as **Aware** if it is confirmed to be the same real
  thing, not a coincidental name match.
- If nGenue-MCP returns nothing, or the ticket clearly describes this
  entity changing or being created in a way the graph could not yet
  reflect (new form, new proc, modified logic pre-testing), classify as
  **Unaware**.

Read `references/mode-classification.md` for the full decision procedure
and the exact nGenue-MCP tools to use per entity type before doing this
stage — it is the most detail-sensitive part of this skill.

## Stage 4 — Gather findings per classification

**For each Aware entity:** pull its full real structure from nGenue-MCP
(columns, parameters, callers, related objects, business description) and
record it as confirmed ground truth.

**For each Unaware entity:** do not guess at what the new/changed object
does. Instead, anchor on the nearest confirmed object it connects to (the
table it likely writes to, the form it's likely bound to, the proc it's
likely adjacent to) and run blast-radius tooling from that anchor —
`get_column_impact`, `get_table_used_by`, `find_forms_using_table`,
`get_procedure_callers`, `get_trigger_blast`, `get_dependent` equivalents.
Record what currently depends on that anchor area, so later skills know
what could be affected even though the new object itself isn't indexed.

## Stage 5 — Write the context file

Write `<TICKET-KEY>_context.md` to the sandbox with this structure:

```markdown
# <TICKET-KEY> Context

## Ticket Summary & Status
## Ticket History / Changelog
## Related & Dev Tickets
## Prior Bugs (Raised / Resolved)
## Domain Entities Identified
## Per-Entity Classification (Aware / Unaware + evidence)
## Aware-Mode Findings (confirmed graph cross-reference)
## Unaware-Mode Findings (blast-radius / affected-nodes analysis)
## Consolidated Knowledge Summary
```

The **Consolidated Knowledge Summary** section is the actual payload the
next skill reads first — write it as a dense, complete brief a test-case
writer could work from without re-reading the rest of the file. Do not
compress it at the expense of accuracy; this is the one section that must
never drop detail.

Confirm to the tester that context has been built, name the file, and
give a one-line count of entities found in each mode (e.g. "4 aware, 2
unaware"). Do not proceed to write test cases unless asked — that is
adversarial-test-writer's job, a separate invocation.
