# Aware / Unaware Classification — Full Procedure

This is the core judgment call of ticket-context-builder. Follow this
procedure for every entity extracted in Stage 2 of SKILL.md.

## Why entity-level, not ticket-level

A single ticket can touch a mix of existing, already-indexed application
pieces and brand-new or freshly modified ones. Treating the whole ticket
as one mode throws away real information: an Aware entity deserves a
confirmed, detailed lookup; an Unaware entity needs blast-radius inference
instead. Mixing them into one ticket-wide mode either wastes the confirmed
data or overstates confidence in the unconfirmed part.

## Step-by-step per entity

1. **Match by tool, not by memory.** Never assume an entity exists or
   doesn't based on general familiarity with the nGenue application. Query
   nGenue-MCP directly every time.

   | Entity type | Primary lookup tool |
   |---|---|
   | Delphi form / data module / frame | `find_form_by_name` |
   | Stored procedure / function | `find_procedure_by_name` |
   | Table / view | `find_table_by_name` |
   | Any SQL object, fuzzy name | `search_sql_objects_by_name` |
   | Business concept / process | `search_data_dictionary` |
   | General description lookup | `get_object_description` |

2. **Confirm, don't assume.** A returned match is only provisional. Pull
   the object's actual description/columns/parameters
   (`get_table_overview`, `get_procedure_overview`, `get_form_overview`)
   and compare against what the Jira ticket actually says this entity is
   for. A name match on a common term (e.g. a generic table name) is not
   sufficient on its own.

3. **Classify:**
   - **Aware** — confirmed real match, cross-referenced successfully
     against ticket intent.
   - **Unaware** — no match found, OR a match exists but the ticket
     describes changes to it that clearly postdate what the graph
     reflects (e.g. ticket says "add new column X to handle Y" — the
     table is Aware as a base object, but the specific change is
     Unaware).

   Note the sub-case above explicitly in the context file: an entity can
   be Aware-as-baseline but Unaware-for-the-specific-change. Record both
   halves rather than forcing a single label.

## Unaware-mode blast-radius procedure

Once an entity is Unaware, do not stop. Anchor on whatever confirmed
object is nearest to it and run:

- `get_column_impact` — if a column is changing/being added
- `get_table_used_by` / `find_forms_using_table` — what currently reads or
  binds to the anchor table
- `get_procedure_callers` / `get_procedure_call_graph` — what currently
  calls into the anchor procedure
- `get_trigger_blast` — what triggers would fire as a consequence
- `get_dependent`-style tools for the anchor's own dependency chain

Record every object surfaced this way under "Unaware-Mode Findings" in the
context file, with a one-line note per object explaining why it's
relevant (e.g. "reads from this table via a lookup field on Form X").

## What "evidence" means in the context file

For every entity, the Per-Entity Classification section must show its
evidence, not just its label:

```
Entity: PNL_SUMMARY table
Mode: Aware
Evidence: Confirmed via find_table_by_name + get_table_overview; ticket
description references "PNL_SUMMARY history" which matches the table's
actual business description ("stores PLEX run results per deal side").
```

```
Entity: New "Curve Shift" recalculation logic
Mode: Unaware
Evidence: No matching procedure found via search_sql_objects_by_name.
Ticket states this is new logic being added to the PLEX run. Anchored on
existing PLEX-related procedure [name] via get_procedure_call_graph to
surface likely blast radius.
```

A classification without evidence is not acceptable output from this
skill — later skills rely on being able to trust or re-check the reasoning
without redoing the lookups themselves.
