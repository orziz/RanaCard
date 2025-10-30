# Repository Guidelines

This file is for agents. Treat it as the source of truth when starting in a fresh session. Follow these rules for the entire repository unless the user explicitly overrides them.

## Project Overview
- Name: RanaCard Assistant (种呱得呱助手)
- Goal: Web UI for viewing, searching, and editing encrypted in‑game data (Card.json, Pendant.json). Users import/export encrypted files; decryption/encryption is server‑side only.

## Structure
- `ui/` Vue 3 + Vite + Element Plus (frontend) — built to `ui/dist/`.
- `server/` FastAPI app (backend) — holds encryption keys; never leak to frontend.
- `Data/` official baseline JSON used for “Load Game Data”.
- `deploy/nginx/` Nginx config for container.
- `docker-compose.yml` one‑command deployment (frontend + backend).

## Run & Dev
- Backend dev: `cd server && pip install -r requirements.txt && uvicorn main:app --reload`
- Frontend dev: `cd ui && npm i && npm run dev` (set `VITE_API_BASE` in `ui/.env` if backend not on default).
- Docker prod: repo root → `docker compose up -d --build` (binds to `127.0.0.1:8080`, use external Nginx to expose).

## API (server)
- `GET /api/data/card|pendant` returns official JSON from `Data/`.
- `POST /api/decode` multipart encrypted file → JSON.
- `POST /api/encode` `{ payload }` → encrypted text (save as game file).
- `POST /api/validate?kind=card|pendant` basic structure checks.

## Security Rules (must‑follow)
- Keys and crypto live only in `server/services/crypto.py`. Do not copy or reimplement crypto in the frontend.
- Keep CORS permissive in dev; prefer same‑origin via Nginx proxy in prod.
- Do not commit secrets; `.gitignore` prevents common leaks (node_modules, dist, venv, logs).

## Editing Model & UX Principles
- Edit only fields that vary across items (derived from tools/analyze_fields.py):
  - Cards: Name, ID, Category, Type, Level, Character, Combo, EffectDescription, EffectString, SpecialVal, _growPeriod, _harvestIncome, _timeLabel, CanGainByPack.
  - Pendants: Name, ID, Character, Combo, Level, EffectDescription, EffectString, ForbidState, CanGainByPack.
- All other fields are editable via “Edit JSON” mode; preserve key order and casing.
- Search must include ID/Name/EffectDescription/EffectString; provide category filters (Cards: Category/Type; Pendants: Character/Combo).

## Conventions
- Python: PEP 8, 4‑space indent, UTF‑8. Keep changes minimal and focused.
- JSON: 2‑space indent; preserve casing and order; avoid schema churn.
- Frontend: TypeScript, Vue SFCs; keep labels in Chinese for user‑facing text.

## Deployment
- Default compose binds `web` to `127.0.0.1:8080`; expose via your server’s Nginx:
  - `location / { proxy_pass http://127.0.0.1:8080/; }`
- Frontend Nginx (in container) proxies `/api` → backend service.
- Update: `git pull && docker compose up -d --build`.

## Do / Don’t
- Do: use backend endpoints for all encode/decode; keep UI simple; validate before export.
- Don’t: add client‑side crypto, rename JSON keys, or commit build artifacts.
