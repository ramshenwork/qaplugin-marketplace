# qaplugin-marketplace

Personal plugin marketplace for QaPlugin — a QA workflow plugin for the
nGenue application (Jira ticket context + adversarial test case writing +
bug consolidation).

## Add this marketplace in Claude Desktop

1. Customize → Plugins → click `+` next to **Personal plugins** → **Add
   marketplace**
2. Paste this repo's GitHub URL
3. Click Sync
4. Find `qaplugin` in the listing → Install

## Updating

Bump `plugins/qaplugin/.claude-plugin/plugin.json`'s `version`, add an
entry to `plugins/qaplugin/CHANGELOG.md`, commit, and push. Cowork
offers the new version on its next sync — no need to reinstall from
scratch.

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json     # catalog Cowork reads
├── plugins/
│   └── qaplugin/            # the plugin itself — see its own README.md
└── README.md
```

See `plugins/qaplugin/README.md` for what the plugin actually does.
