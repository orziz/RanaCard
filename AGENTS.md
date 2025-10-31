# Repository Guidelines

Concise guide for contributors and agents working in this repo.

## Project Structure & Module Organization
- `ui/` Vue 3 + Vite + Element Plus (built to `ui/dist/`).
- `server/` FastAPI backend; crypto lives here only.
- `Data/` official baseline JSON for “Load Game Data”.
- `deploy/nginx/` container Nginx config; `docker-compose.yml` orchestrates web+api.

## Build, Test, and Development Commands
- Backend dev: `cd server && pip install -r requirements.txt && uvicorn main:app --reload`.
- Frontend dev: `cd ui && npm i && npm run dev` (set `VITE_API_BASE` in `ui/.env` when not same-origin).
- Docker prod: repo root → `docker compose up -d --build` (binds `127.0.0.1:8080`).
- Validate data: `POST /api/validate?kind=card|pendant` before encode/export.

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indent, UTF‑8; minimal, focused diffs.
- Frontend: TypeScript + Vue SFCs; user‑facing labels in Chinese.
- JSON: 2‑space indent; preserve key order/casing; avoid schema churn.
- Editing model: expose only variable fields; advanced edits via “Edit JSON” while preserving order.

## Testing Guidelines
- No formal test suite yet. Prefer API+UI validation:
  - Use `/api/validate` and manual flows (import → edit → validate → encode → export).
  - Keep PRs small to ease manual verification.

## Commit & Pull Request Guidelines
- Use Conventional Commits seen in history: `feat(scope): …`, `fix(scope): …`, `chore(scope): …` (e.g., `feat(ui):`, `fix(docker):`).
- PRs: clear description, linked issues, repro steps; include UI screenshots/GIFs when applicable.
- Do not commit build artifacts, secrets, or local env files.

## Security & Configuration Tips
- Never implement crypto in the frontend; keys and algorithms stay in `server/services/crypto.py`.
- In dev allow CORS; in prod prefer same‑origin via Nginx proxy.
- Always use backend for `encode`/`decode`; never expose keys or intermediate secrets.
