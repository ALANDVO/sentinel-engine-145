# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

Completed channel-registry feature:
- Base Channel abstract class with search/fetch/health_check interface
- ChannelRegistry for managing channels (register, unregister, get, list)
- MockChannel implementation for testing with call tracking
- SearchResult dataclass for structured search results
- 24 new tests covering channel registry and mock channel
- All 29 tests passing (5 original + 24 new)
- Ruff linting clean (only acceptable style warnings remain)

## 1.1.0 — work-in-progress checkpoint

Completed core skeleton:
- FastAPI application with `/health` and `/` endpoints
- Typer CLI with `version`, `config-show`, and `--help` commands
- Configuration module with platform configs and YAML/env loading
- Unit tests for health endpoints and CLI commands (5 tests passing)
- Ruff linting clean

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
