# AIOS Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Ship the complete single-owner AIOS platform described by `IMPLEMENTATION-PLAN.md), with Mission Control and Scout/Operator/Advisor as the finished student-facing experience.

**Architecture:** Build the platform on the implementation plan's server-first architecture: FastAPI, plain HTML/JavaScript, validated Markdown skills, file-backed metrics, scheduled collectors, and owner-controlled connectors. Add the Google Doc's Mission Control experience and three core roles without replacing the plan's seven wings, vault, panels, or 150-agent library.

**Tech Stack:** Python 3.11+, FastAPI, Uvicorn, PyYAML, standard-library scripts, plain HTML/CSS/JavaScript, JSONL/JSON files, Python SVG rendering, Telegram Bot API, Groq, ElevenLabs, Composio, Blotato, and optional Node 18+ archify tooling.

**Spec:** `docs/superpowers/specs/2026-09-08-aios-platform-design.md`

## Global Constraints

- Students configure a finished platform; they do not write platform code.
- `IMPLEMENTATION-PLAN.md` is the source of truth for scope, file names, commands, and checks.
- The dashboard uses FastAPI plus one HTML file and one JavaScript file; no React, npm, or dashboard build step.
- Dashboard routes require HTTP Basic auth with username `owner` and `DASHBOARD_PASSWORD`; no default password.
- The dashboard reads generated files and never calls third-party APIs on page load.
- Every metric carries source, timestamp, and status; unavailable data is never replaced with zero or an estimate.
- Draft before send; approval is required for publishing, money, refunds, legal matters, and external data changes.
- Secrets never enter Git, logs, generated map data, or screenshots.
- Composio uses the current Python `composio` package and an MCP-enabled session; generated settings remain untracked.
- Every implementation task adds a focused automated or fixture test before production code.

---

### Task 1: Build 0 — runtime, secrets, and bootstrap

**Files:**
- Create: `config/models.yaml`, `config/route.yaml`, `scripts/bootstrap.py`, `scripts/preflight.py`, `scripts/usage_report.py`
- Modify: `.env.example`, `.gitignore`, `requirements.txt`, `INSTALL.md`
- Test: `tests/test_bootstrap.py`, `tests/test_preflight.py`

**Interfaces:**
- `load_route() -> dict`
- `validate_environment(route: dict, environ: Mapping[str, str]) -> list[str]`
- `bootstrap_install(root: Path) -> None`
- `usage_report(records: Iterable[dict]) -> dict`

- [ ] Write failing tests for missing-password refusal, forbidden `ANTHROPIC_API_KEY`, route validation, secret-file permissions, and repeatable bootstrap.
- [ ] Run the focused tests and verify they fail because the runtime modules do not exist.
- [ ] Implement the smallest route/preflight/bootstrap modules required by the tests.
- [ ] Run the focused tests, then the full Python test suite.
- [ ] Verify a clean bootstrap from a temporary directory and record the command/output in the task notes.

### Task 2: Build 1 — skill registry, validator, map, server, and activity log

**Files:**
- Create: `references/tool-registry.md`, `scripts/validate_skills.py`, `scripts/build_map.py`, `scripts/activity.py`, `dashboard/server.py`, `dashboard/requirements.txt`, `dashboard/static/index.html`, `dashboard/static/app.js`
- Modify: `skill-vault/*/SKILL.md`, `.gitignore`
- Test: `tests/test_validate_skills.py`, `tests/test_build_map.py`, `tests/test_activity.py`, `tests/test_dashboard_api.py`

**Interfaces:**
- `validate_skill(path: Path) -> list[str]`
- `build_map(root: Path) -> dict`
- `log(event: str, skill: str | None = None, detail: str | None = None, status: str = "ok") -> None`
- `GET /api/map`, `GET /api/skill/{name}`, `GET /api/activity`, `GET /api/health`, `POST /api/run`

- [ ] Write tests for frontmatter rejection, metadata contract, stable map ordering, redaction/rotation, Basic auth, skill allowlisting, and deliberate empty states.
- [ ] Run the tests and verify red failures for the missing validator, map, logger, API, and page.
- [ ] Implement the registry, validator, map generator, activity log, authenticated API, and Mission Control fallback page.
- [ ] Run focused tests, generate a fixture map, and open the dashboard against fixture data.
- [ ] Verify unauthenticated requests return 401, invalid skills return 400, and a fresh install renders invitations instead of blank/zero cards.

### Task 3: Build 2 — voice and remote Command Wing

**Files:**
- Modify: `scripts/bridge.py`, `.env.example`, `curriculum/days/day-6.md`, `curriculum/00-SERVICES-AND-SETUP.md`
- Test: `tests/test_bridge.py`, `tests/fixtures/telegram_updates.json`

**Interfaces:**
- `speak(text: str) -> bytes | None`
- `send_voice(chat_id: str, mp3_bytes: bytes) -> None`
- `ask_claude(prompt: str) -> str`

- [ ] Write tests for text-only fallback, voice transcription, ElevenLabs failure fallback, Telegram multipart encoding, chat locking, and redacted activity events.
- [ ] Run the tests and verify red failures.
- [ ] Implement voice output with ffmpeg conversion and always preserve the text response.
- [ ] Run the bridge tests and a fixture-backed one-shot update loop.
- [ ] Verify the curriculum instructions match the working command and optional-key behavior.

### Task 4: Build 3 — complete agent library and core roles

**Files:**
- Create: `skill-vault/scout/SKILL.md`, `skill-vault/operator/SKILL.md`, `skill-vault/advisor/SKILL.md`, `context/templates/faq.md`, `context/templates/about-business.md`, `scripts/run_role.py`
- Modify: all shipped `skill-vault/*/SKILL.md` files and `references/agent-spec.md`
- Test: `tests/test_agent_library.py`, `tests/fixtures/core_role_inputs/`

**Interfaces:**
- `run_scout(inputs: dict) -> dict`
- `run_operator(request: dict, context: dict) -> dict`
- `run_advisor(scout: dict, operator: dict) -> dict`
- `validate_library(root: Path) -> dict`

- [ ] Write fixture tests for source/date preservation, `UNAVAILABLE`, exactly three recommendations, FAQ escalation, approval gates, and metadata completeness.
- [ ] Run the tests and verify red failures.
- [ ] Convert every shipped skill to the metadata contract, add the three roles, and implement deterministic fixture orchestration.
- [ ] Run library validation and fixture runs.
- [ ] Verify the generated map contains every shipped skill and the core roles.

### Task 5: Build 4 — connectors and Composio

**Files:**
- Create: `scripts/connector.py`, `scripts/collect.py`, `scripts/create_composio_session.py`, `references/connector-contract.md`
- Modify: `requirements.txt`, `.gitignore`, `references/composio-setup.md`, `curriculum/days/day-5.md`
- Test: `tests/test_connectors.py`, `tests/test_composio_config.py`

**Interfaces:**
- `ConnectorResult(value: object, source: str, collected_at: str, status: str, error: str | None)`
- `load_connector(name: str, environ: Mapping[str, str]) -> Connector`
- `write_mcp_config(url: str, headers: Mapping[str, str], path: Path) -> None`

- [ ] Write tests for missing keys, source/timestamp/status preservation, error rows, valid JSON with multiple headers, and ignored local MCP settings.
- [ ] Run the tests and verify red failures.
- [ ] Implement the generic connector boundary, Composio MCP session using `composio` with `mcp=True`, and safe config generation.
- [ ] Run focused tests and verify no secret-bearing settings file is tracked.
- [ ] Verify optional services degrade to explicit unavailable states.

### Task 6: Build 5 — vault, document ingestion, local search, installer, schedules

**Files:**
- Create: `vault/`, `scripts/ingest.py`, `scripts/search_vault.py`, `scripts/interview.py`, `scripts/install_server.py`, `scripts/schedule.py`
- Modify: `.gitignore`, `requirements.txt`, `INSTALL.md`, `curriculum/days/day-0.md`
- Test: `tests/test_ingest.py`, `tests/test_vault_search.py`, `tests/test_install_server.py`

**Interfaces:**
- `ingest(path: Path, vault_root: Path) -> dict`
- `search(query: str, vault_root: Path) -> list[dict]`
- `install_server(root: Path, env: Mapping[str, str]) -> dict`
- `schedule_jobs(root: Path, jobs: list[dict]) -> None`

- [ ] Write tests for PDF/text ingestion, no-secret vault paths, keyword/local-model fallback, idempotent installation, and cron/systemd output.
- [ ] Run the tests and verify red failures.
- [ ] Implement encrypted/permissioned storage boundaries, pypdf extraction, local search adapter, interview flow, installer, and schedule definitions.
- [ ] Run the focused tests and a temporary-server install.
- [ ] Verify a fresh student setup needs configuration only and never source edits.

### Task 7: Build 6 — metrics, charts, diagrams, panels, and Mission Control roles

**Files:**
- Create: `scripts/chart.py`, `scripts/diagram.py`, `panels/*.yaml`, `scripts/panel.py`, `dashboard/static/fixtures/mission-control.json`
- Modify: `scripts/collect.py`, `dashboard/server.py`, `dashboard/static/index.html`, `dashboard/static/app.js`
- Test: `tests/test_chart.py`, `tests/test_panels.py`, `tests/test_mission_control.py`

**Interfaces:**
- `render_chart(spec: dict, rows: list[dict]) -> str`
- `collect_card(card: dict, connectors: dict) -> dict`
- `render_panel(panel: dict, metrics: dict) -> dict`
- `build_mission_control(scout: dict, operator: dict, advisor: dict, metrics: dict) -> dict`

- [ ] Write tests for all five chart shapes, source/timestamp labels, error rows, seven panel schemas, empty states, and Scout/Operator/Advisor rendering.
- [ ] Run the tests and verify red failures.
- [ ] Implement append-only metrics, SVG/PNG rendering, diagram fallback, YAML-driven panels, and the unified Mission Control view.
- [ ] Run focused tests, render charts, and load the dashboard with fixture data.
- [ ] Verify the dashboard and Telegram consume the same metric/chart payloads.

### Task 8: Build 7 — curriculum and student acceptance

**Files:**
- Modify: `curriculum/README.md`, `curriculum/days/day-0.md` through `day-7.md`, `curriculum/00-SERVICES-AND-SETUP.md`, `curriculum/troubleshooting.md`
- Create: `scripts/student_acceptance.py`, `tests/test_student_acceptance.py`
- Test: `tests/fixtures/student-run/`

**Interfaces:**
- `run_acceptance(root: Path) -> dict`
- `validate_curriculum_links(root: Path) -> list[str]`

- [ ] Write acceptance tests for a clean install, each day's configuration gate, connection verification, no-code student flow, and final inspection.
- [ ] Run the tests and verify red failures.
- [ ] Rewrite instructions so every platform component already exists before Day 0.
- [ ] Run the complete acceptance suite from a temporary clean installation.
- [ ] Verify every required command, link, environment variable, and output in the curriculum.

## Final verification

- [ ] Run the full Python test suite.
- [ ] Run skill validation across the entire library.
- [ ] Run map generation from a clean context directory.
- [ ] Start the authenticated dashboard and verify all API routes.
- [ ] Run fixture Scout, Operator, and Advisor workflows.
- [ ] Run the connector/configuration safety checks.
- [ ] Run the clean-install student acceptance suite.
- [ ] Compare every completion item in `IMPLEMENTATION-PLAN.md` and Appendix C against fresh evidence.
