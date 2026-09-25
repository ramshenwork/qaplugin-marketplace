# Changelog

## 0.1.1
- Fixed invalid YAML frontmatter in `agents/domain-knowledge-agent.md`.
  The `description` field used a folded block scalar (`>`) with unindented
  `<example>` blocks below it — the block scalar terminated at the first
  0-indent line, leaving `<example>` to be parsed as an invalid bare
  mapping key. Rebuilt as a literal block scalar (`|`) with every line,
  including the examples, indented under the key. Verified against
  PyYAML directly, not just visually.

## 0.1.0
Initial release.
- `ticket-context-builder`: Jira + nGenue-MCP context gathering with
  entity-level Aware/Unaware classification.
- `adversarial-test-writer`: exhaustive seven-category test case
  generation, fixed xlsx output format matching MNLN-23205 reference
  sample.
- `bug-consolidator`: root-cause tracing, failure consolidation, Jira
  comment/ticket routing with mandatory tester confirmation on every
  write.
- `domain-knowledge-agent`: shared live sub-agent for Atlassian and
  nGenue-MCP lookups across all three skills.
