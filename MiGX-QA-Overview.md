# MIGx QA Challenge — Submission Overview

Two repositories cover the full challenge:

| Part | Repo (folder) | Stack | Tests |
|------|---------------|-------|-------|
| **UI** | SauceDemo (Playwright) | Playwright + playwright-bdd (Cucumber) + TypeScript | 17 |
| **API** | `api-migx` (ReqRes) | pytest + requests + jsonschema (Python) | 17 |

> Two separate repos on purpose: different layer, tool, language and run speed.
> Each runs independently; link them from each README so a reviewer sees both.

---

## 1. UI suite — SauceDemo (Playwright + BDD)

**What it covers (17 tests):**
- **Login & access control** (project `guest`, no session): standard login, locked-out, invalid password, empty username, empty password.
- **Sorting** (project `authed`): Name A–Z / Z–A, Price low–high / high–low.
- **Cart** (authed): add single, remove.
- **Checkout** (authed): complete order, totals = item + tax, empty first/last/postal validation.
- **Auth reuse**: a `setup` project logs `standard` + `problem` in once and saves `.auth/<role>.json` (storageState); authenticated flows reuse the session.

**Run:**
```bash
npm install
npx playwright install --with-deps chromium
npm test                 # bddgen + run all projects
npm run report           # HTML report
```

**Key design:**
- Page Object Model (`BasePage` + one class per page), assertions live in step definitions.
- `data-test` locators (`testIdAttribute`), web-first assertions, **no hardcoded waits**.
- Test data in JSON (`users.json`, `products.json`) resolved via `userByKey` / `productByName`.
- Env base URL via `environmentBaseUrl` (`ENV` / `BASE_URL`).

**Docs (in the UI repo `docs/`):** `test-plan.md`, `test-case-matrix.md`, `defect-log.md`, `bug-report.md`.

---

## 2. API suite — ReqRes (pytest + requests)

**What it covers (17 tests):**
- **/users**: list (`?page=2`), single, 404, create (POST), update (PUT/PATCH), delete, delayed response.
- **/register + /login**: success + negative (missing password / email / empty body).
- **/unknown**: resource list + 404.

**3-layer assertions:** status code → JSON schema (jsonschema draft-07) → semantics (echoed fields, ISO timestamps, email format).

**Run:**
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
py -m pytest                    # 17 tests + HTML report (reports/api-report.html)
py -m pytest -m smoke           # fast subset
```

**Layout:** `conftest.py` (fixtures) · `utils/api_client.py` (requests.Session wrapper: base URL, `x-api-key`, timeout) · `schemas/` (draft-07) · `tests/`.

**Config:** `REQRES_BASE_URL` + `REQRES_API_KEY` from `.env` (python-dotenv). `.env` is gitignored — the real key stays private. Free tier ~40 req/day per IP; `429` = quota, not a test failure.

---

## 3. Coverage vs the challenge

| Requirement | Status |
|-------------|--------|
| Test Plan + test-case matrix | ✅ `docs/` |
| Manual / exploratory + defect log | ✅ `docs/defect-log.md` |
| Automated regression (login + checkout min) | ✅ UI suite, 17 tests |
| API suite (status / schema / errors) | ✅ API suite, 17 tests |
| Bug report (DevTools evidence) | ✅ `docs/bug-report.md` (DEF-02) |
| README (setup, run, strategy) + bonus Q&A | ✅ both repos |

---

## 4. Bonus answers (summary — full text in UI README)
1. **CSV/GxP:** Validation Plan + URS/FRS + RTM; IQ (install), OQ (these functional tests), PQ (real-world), evidenced under change control + audit trail.
2. **CI/CD:** GitHub Actions — install + browsers, run suite, publish HTML + trace artifacts; `@smoke` on PR (merge gate), full `@regression` nightly / on merge.
3. **Test data:** typed catalogs; fresh browser context per test + storageState reuse; for stateful apps seed/reset via API/DB fixtures, unique data, teardown.
4. **Non-functional:** page-load timing (perf_glitch signal), Lighthouse; axe-core a11y on login/checkout.
5. **Risk-based (4h):** automate deterministic money path (login/cart/checkout/sorting) + API contract; explore seeded per-user defects manually; defer cross-browser/visual/full-a11y.

---

## 5. AI transparency
AI tooling (Claude) was used to accelerate scaffolding, refactors and documentation.
All technical decisions (POM, storageState, env config, prioritization, schema design)
are the author's and can be explained end-to-end.

---

## 6. Submission checklist
- [ ] Push UI repo (public) — README complete
- [ ] Push API repo (public) — README complete
- [ ] Cross-link the two READMEs
- [ ] (Private repo) invite `MIGx-user`
- [ ] Email the GitHub link(s)
