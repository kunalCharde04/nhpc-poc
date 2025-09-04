# Medical Bill Validation Backend (FastAPI) — with Authentication

AI-powered backend for extracting, processing, and validating medical bills against supporting documents. Includes JWT-based authentication to protect all business endpoints.

## Quick Start

1) Install dependencies
```bash
cd "./bill-validator-backend"
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

2) Start AI service (separate terminal)
```bash
cd "../ai-service"
python start.py
```

3) Start backend
```bash
cd "./bill-validator-backend"
python start.py
```

Backend runs at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

## Configuration

Environment variables (optional):
- `AI_SERVICE_URL` (default `http://localhost:8001`)
- `APP_HOST` (default `0.0.0.0`)
- `APP_PORT` (default `8000`)

## Authentication

- Auth is JWT (HS256). Tokens are short strings returned by `/auth/login` and must be sent as `Authorization: Bearer <token>`.
- Users are stored in a local SQLite DB at `bill-validator-backend/auth.db` using SQLAlchemy. Table: `users(id, username, password_hash, is_active, created_at)`.
- Registration is not exposed in the UI. Use curl to create users.

### Create user (register via curl only)
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"StrongPass123!"}'
```

### Login (get token)
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=admin&password=StrongPass123!' \
  | jq
```
Response:
```json
{ "access_token": "<JWT>", "token_type": "bearer" }
```

### Use token
Add header `Authorization: Bearer <JWT>` to all protected endpoints below.

## Endpoints

Public:
- `GET /` — Health/info
- `GET /health` — Detailed health
- `POST /auth/register` — Create user (restricted to curl usage)
- `POST /auth/login` — Obtain JWT

Protected (require Bearer token):
- `POST /extract-bills` — Upload bill entries PDF/image; returns structured entries. Multipart: `bill_entries_file=@...` and optional repeated `supporting_documents=@...`
- `POST /process-documents` — Upload supporting documents only
- `POST /validate-bills` — JSON flow to validate using preprocessed arrays

### Example: extract bills
```bash
TOKEN="<paste-token>"
curl -X POST http://localhost:8000/extract-bills \
  -H "Authorization: Bearer $TOKEN" \
  -F "bill_entries_file=@/path/to/bills.pdf" \
  -F "supporting_documents=@/path/to/doc1.pdf" \
  -F "supporting_documents=@/path/to/doc2.jpg"
```

### Example: validate with JSON
```bash
TOKEN="<paste-token>"
curl -X POST http://localhost:8000/validate-bills \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bill_entries": [...], "processed_documents": [...]}'
```

## Tech Notes

- Framework: FastAPI
- Auth: `python-jose` (JWT), `passlib[bcrypt]` for hashing
- DB: SQLite via SQLAlchemy (`sqlite:///./auth.db`)
- File handling: `python-multipart`
- AI calls: `aiohttp` to the local AI service

## Development

- Dependencies are pinned in `requirements.txt`.
- On first run, the users table is created automatically.
- If you need to reset users, stop the server and delete `auth.db`.
