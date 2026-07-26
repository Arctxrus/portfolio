# PROGRESS — Zayn Portfolio

Stage log, decisions and deviations for the build defined in CONCEPT.md.
House rules: UK English, no em dashes, instrument then fix, commit per stage.

## Open items

- [ ] Replace placeholder email. `hello@placeholder.invalid` is used everywhere the
      spec says REPLACE email. It lives in a single constant (`SITE_EMAIL` in
      js/main.js, mirrored once in index.html for the no-JS footer text). Swap
      before deploy.
- [ ] Panel sub lines for the three projects: drafted at stage 3, need approval.
- [ ] About and Pricing prose: drafted at stage 3, need approval.
- [ ] docs/de-vibe-audit.md: the agreed checklist was not supplied in this
      workspace. A draft checklist will be written at stage 8 and submitted for
      approval before the audit runs.
- [ ] Formspree endpoint ID: form is wired with a placeholder endpoint constant;
      real ID needed before deploy.
- [ ] Stage 6 video capture depends on the live demo sites and headed Chromium
      with GPU; may be marked blocked with exact local commands.
- [ ] Stage 10 waits on the confirmed deployed URL.

## Decisions and deviations

- 2026-07-26: Agent files requested with model "claude-opus-5" for the coder.
  No such model exists; the coder is set to `opus` (resolves to the latest
  Opus, currently 4.8). Verifier and triage use `sonnet` (Sonnet 5) as asked.
- 2026-07-26: Email placeholder `hello@placeholder.invalid` adopted per
  instruction, single-constant, listed above as an open item.

## Stage log

### Setup (2026-07-26)
- Repo initialised, GitHub repo Arctxrus/portfolio created, CONCEPT.md committed.
- PROGRESS.md, verify/, references/REFERENCES.md created.
- Agent team created in .claude/agents/ (coder, verifier, triage).

### Stage 1 — Scaffold
- Status: pending.
