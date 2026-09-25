# QaPlugin

QA workflow plugin for the nGenue application: builds full ticket +
application context from Jira and nGenue-MCP, writes exhaustive
adversarial test cases in a fixed xlsx format, and consolidates failed
results into root-caused, debug-ready bug reports routed back to Jira —
every Jira write gated on explicit tester confirmation.

## Components

**Connectors**
- Atlassian (Jira) — ticket details, history, links, comments, ticket
  creation
- nGenue-MCP — application structure lookups and blast-radius tracing
  across Delphi forms, SQL objects, and business/domain logic

**Skills**
- `qaplugin:ticket-context-builder` — pulls full ticket knowledge from
  Jira, classifies every referenced application entity as Aware (graph
  already knows it) or Unaware (graph predates this change) at the
  entity level, and writes `<TICKET-KEY>_context.md` to the sandbox.
  Read-only.
- `qaplugin:adversarial-test-writer` — reads a ticket's context file and
  writes every test case it can reason out across seven categories
  (Positive, Negative, Boundary/Edge, State & Sequence, Regression,
  Blast-radius/Collateral, Concurrency) with the explicit goal of
  breaking the change, not confirming it. Outputs an xlsx matching a
  fixed reference format exactly, built through a bundled script rather
  than freehand formatting. Read-only.
- `qaplugin:bug-consolidator` — takes the tester's completed xlsx back,
  root-causes every marked failure using live nGenue-MCP trace tooling,
  consolidates failures sharing one root cause into a single bug, and
  writes a debug-ready report. Routes in-scope bugs as a comment on the
  existing ticket, out-of-scope bugs as a new ticket. Both write paths
  require the tester's explicit go-ahead before anything is posted.

**Agents**
- `domain-knowledge-agent` — standing live access to both connectors,
  delegated to by any skill mid-run when it needs a fact not already in
  the stored sandbox context. Read-only; never writes.

## Setup

Both connectors (Atlassian, nGenue-MCP) must already be connected in
Claude for this plugin to function — the plugin references them by name
and does not manage authentication itself.

## Usage

Typical flow for one ticket:

1. "Pull context for TICKET-123" → ticket-context-builder
2. "Write test cases for TICKET-123" → adversarial-test-writer, produces
   the xlsx
3. Run the cases manually against the nGenue application, mark results in
   the xlsx, hand it back
4. "Here are my test results" (with the marked-up xlsx) →
   bug-consolidator, produces root-caused reports and drafts Jira writes
   for your confirmation

## Governance

- Single-owner-with-change-request: this plugin has one owner; changes
  route through them, versioned MAJOR.MINOR.PATCH with `CHANGELOG.md`.
- No mid-run hot-swapping: a version update should not land mid-session
  while a skill is actively drafting or writing to Jira.
- No Jira write ever happens without explicit tester confirmation shown
  against the exact draft being posted — this is enforced in
  bug-consolidator's own instructions, not just documented here.
