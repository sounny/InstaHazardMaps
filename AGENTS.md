# AGENTS.md

This repository uses Codex agents. Use this file to build a lightweight memory for future agents.

## Instructions
- Review this file before starting work.
- After each commit, append a bullet under **Log** summarizing what you changed.
- Add any new thoughts or follow-up ideas under **Ideas**.
- Keep the newest bullets at the top of each list.

## Log
- Added a styled IMH startup banner for interactive CLI sessions, with JSON-safe suppression and `HAZARDWATCH_NO_BANNER` opt-out; expanded CLI tests and README docs.
- Improved CLI UX with new `sources`/`plan` subcommands, `--version`, and terminal install packaging via `pyproject.toml`; refreshed README install guidance and CLI tests.
- Added a dedicated `hazardwatch` CLI `search` command with human/JSON output, plus README usage docs and CLI tests.
- Created `AGENTS.md` with logging instructions.

## Ideas
- Add a `--no-banner` CLI flag for one-off suppression without setting environment variables.
- Add a `doctor` command that validates Python deps, AOI readability, and STAC connectivity before running a search.
- Add additional subcommands like `plan`, `sources`, and `export` to make the tool feel closer to Codex CLI workflows.
- 
