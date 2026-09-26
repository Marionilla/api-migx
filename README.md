# MIGx QA Challenge — ReqRes API Test Suite

### Companion UI test suite (SauceDemo / playwright): https://github.com/Marionilla/MiGX

---
---


Contract tests for the **ReqRes API** (<https://reqres.in/api>) built with
**pytest + requests + jsonschema**. This is the API half of the MIGx QA
Challenge; the UI half (SauceDemo / Playwright) lives in a separate repository.

> **AI assistance (transparency).** AI tooling (Claude) was used to accelerate
> scaffolding and documentation. All technical decisions (client design, schema
> validation, fixtures, prioritization) are mine and I can explain every part.

---

## Stack
- **pytest** — test runner + fixtures + markers
- **requests** — HTTP client
- **jsonschema** (draft-07) — response-schema validation
- **pytest-html** — self-contained HTML report
- **python-dotenv** — environment configuration

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
copy .env.example .env            # optional (Windows) — cp on macOS/Linux
```

## Run
```bash
py -m pytest                      # all tests + HTML report -> reports/api-report.html
py -m pytest -m smoke             # fast, high-value subset
py -m pytest -m "auth and negative"   # slice by marker
py -m pytest tests/test_users.py -v   # a single file
```
Open the report: `reports/api-report.html`.

## What it validates — 3 layers
Every response is checked at three widening layers, so a failure localises the drift:
1. **Status code** — the coarsest contract (`200 / 201 / 204 / 400 / 404`).
2. **JSON schema** — structural contract (required keys, types, formats) via `jsonschema`.
3. **Semantics** — values the schema can't express (echoed fields, email format, ISO-8601 timestamps).

## Coverage — 17 tests
| Area | Cases |
|------|-------|
| `/users` | list (`?page=2`), single, 404, create (POST), update (PUT), update (PATCH), delete, delayed response — **8** |
| `/register` + `/login` | success + negative (missing password / email / empty body) — **7** |
| `/unknown` (resources) | list + 404 — **2** |

## Layout
```
api-migx/
├─ conftest.py            # fixtures: base_url, api_key, client, validate_schema
├─ utils/
│  └─ api_client.py       # requests.Session wrapper (base URL, x-api-key, timeout)
├─ schemas/
│  └─ reqres_schemas.py   # draft-07 response schemas
├─ tests/
│  ├─ test_users.py
│  ├─ test_auth.py
│  └─ test_resources.py
├─ pytest.ini             # markers, discovery, HTML report
├─ requirements.txt
└─ .env.example
```

## Configuration
`REQRES_BASE_URL` and `REQRES_API_KEY` are read from `.env` (via python-dotenv);
sensible defaults apply if no `.env` is present. `.env` is gitignored — a real
key stays private.

> **Rate limit:** the ReqRes free tier allows ~40 requests/day per IP. When
> exhausted, calls return **429** — that is an environment limit, not a test
> failure. Use your own free API key in `.env` to raise the limit.

## Markers
`smoke`, `regression`, `users`, `auth`, `resources`, `negative` — run slices with
`pytest -m "<expr>"` (e.g. `pytest -m "users and not negative"`).

## Design notes
- **ApiClient** centralizes transport (base URL, `x-api-key` header, default
  timeout, one session) so tests stay declarative — they describe *what* to
  request and assert, never repeat HTTP plumbing.
- **Fixtures** (`conftest.py`) provide a session-scoped client and a
  `validate_schema` helper (draft-07 + `FormatChecker`, path-qualified errors).
- **ReqRes is a stateless mock** — writes don't persist, so tests assert the
  *contract shape* of the response, never a subsequent read; every test is
  idempotent and re-runnable
