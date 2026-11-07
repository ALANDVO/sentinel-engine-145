# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-skeleton

## Roadmap

### core-skeleton — Core FastAPI/React skeleton with CLI entry point

Status: done

Acceptance:
- FastAPI server starts and serves health endpoint
- CLI entry point 'sentinel-engine' runs and shows help
- Basic project structure with pyproject.toml, config, and CLI module
- Unit tests for health endpoint and CLI help

Implementation: `pyproject.toml`, `src/sentinel_engine/__init__.py`, `src/sentinel_engine/main.py`, `src/sentinel_engine/cli.py`, `src/sentinel_engine/config.py`, `tests/test_health.py`, `tests/test_cli.py`

Tests: `tests/test_health.py`, `tests/test_cli.py`

### channel-registry — Channel registry and base channel classes

Status: planned

Acceptance:
- Base Channel class with search/fetch interface
- Channel registry to manage available channels
- At least one mock channel implementation for testing

### search-workflow — End-to-end search workflow (CLI -> API -> Channel -> Results)

Status: planned

Acceptance:
- CLI 'search' command queries channels and returns results
- API endpoint '/search' accepts query and returns aggregated results
- Integration test covering full flow

### platform-adapters — Platform adapters (Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu)

Status: planned

Acceptance:
- Adapter base class and registry
- At least 3 platform adapters with mock implementations
- Adapter health check via doctor command

### config-management — Configuration management (YAML config, env vars, configure command)

Status: planned

Acceptance:
- YAML config file at ~/.sentinel-engine/config.yaml
- CLI 'configure' command to set keys
- Environment variable export command

### doctor-command — Doctor command for health checks

Status: planned

Acceptance:
- Doctor command checks all channels and adapters
- Reports active_backend for each platform
- JSON output option for scripting

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
