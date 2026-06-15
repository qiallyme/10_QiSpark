# Local Development Setup

## Canonical Local Paths

- backend app root: `C:\QiLabs\60_QiApps\_qilife\backend`
- frontend app root: `C:\QiLabs\60_QiApps\_qilife\frontend`
- SQLite database path: `C:\QiLabs\60_QiApps\_qilife\data\db\qilife.sqlite`

## Backend

1. Create and activate a virtual environment.
2. Install backend dependencies from `requirements.txt`.
3. Start FastAPI with `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`.

Python's standard library already includes SQLite support; do not add `sqlite3` as a pip dependency.

## Frontend

1. Install dependencies in `frontend/`.
2. Optional: set `VITE_API_BASE_URL=http://127.0.0.1:8000`.
3. Start Vite on `127.0.0.1:5173`.

If `VITE_API_BASE_URL` is not set, the app stays operational in localStorage fallback mode.

## Deployment Doctrine

We use a single API base URL strategy across environments.

- Frontend app: hosted on Cloudflare Pages.
- Backend app: hosted on `qiserver` running the real FastAPI application with local SQLite.
- Optional gateway: a future Cloudflare Worker may proxy traffic, but it is not the primary backend today.

### Frontend API Configuration

- Uses `VITE_API_BASE_URL` for all backend API calls.
- Local dev example: `http://127.0.0.1:8000`
- Future `qiserver` API target: `https://qilife-api.qially.com`
- Do not hardcode localhost in frontend components.
- On startup, the frontend checks `/api/health`. If offline, it shows `Local fallback mode` and uses localStorage for the working loop.

## Development Rules

- Treat repo `docs/` as canonical system knowledge.
- Keep imported repo docs read-only in the app.
- Do not create a separate wiki service for v1.
