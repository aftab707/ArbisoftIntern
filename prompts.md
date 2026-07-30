# Prompts Log

This file logs every significant prompt used with Claude Code to scaffold, build,
and test this project across the Arbisoft Internship Program 2026, per the
program's AI Coding Ground Rules.

Format per entry: **Prompt**, what Claude did, and any correction applied if the
AI output was wrong.

---

## 2026-07-27

### 1. Scaffold the project

**Prompt:**
> in my folder arbisoft intern there is another folder named week1 in that
> folder create a project of react vite in react js and Include ESLint and
> Prettier for linting and formatting. Run npm install afterwards to make sure
> all dependencies are ready.

**Result:** Scaffolded a React + Vite app in `Week1/` via `npm create vite@latest`.

**Correction applied:** The current Vite React template ships with `oxlint`
instead of ESLint by default. Since ESLint + Prettier were explicitly requested,
removed `oxlint` and its config, and added a proper ESLint 9 flat config
(`eslint.config.js`) with `eslint-plugin-react`, `eslint-plugin-react-hooks`,
`eslint-plugin-react-refresh`, and `eslint-config-prettier`, plus `.prettierrc.json`
and `.prettierignore`. Ran `npm install` and verified `npm run lint`,
`npm run format:check`, and `npm run build` all pass.

**Correction applied (bug found during verification):** Bare ESLint's
`no-unused-vars` rule does not recognize JSX-only usage (e.g. `<StrictMode>`,
`<App />`) without `eslint-plugin-react`'s `jsx-uses-vars` behavior, so
`main.jsx` was falsely flagged as having unused imports. Installed
`eslint-plugin-react` and added its `recommended` + `jsx-runtime` rule sets to
`eslint.config.js` to fix this.

**Correction applied (real lint finding, not a false positive):** The
scaffolded `App.jsx` boilerplate used `target="_blank"` links without
`rel="noreferrer"` (a real `react/jsx-no-target-blank` security finding). Fixed
via `eslint --fix`, then ran `prettier --write .` to normalize formatting.

---

### 2. Initialize git and push to GitHub

**Prompt:**
> Initialize git in ArbisoftIntern folder, commit all current files with the
> message 'Initial commit: React Vite setup', add the remote origin
> git remote add origin https://github.com/aftab707/ArbisoftIntern.git , and
> push to main branch.

**Result:** Ran `git init` in `D:\ArbisoftIntern` (repo root, one level above
`Week1/`), staged all files (`Week1/node_modules` excluded via `Week1/.gitignore`),
committed with the requested message, added the `origin` remote, renamed the
branch to `main`, and pushed with `git push -u origin main`.

---

### 3. Build Week 1 assignment features

**Prompt:**
> [Uploaded internship program outline PDF] ... Add React Router DOM. Create a
> shared Layout with a Navbar, and set up 3 pages/routes: Home, About, and
> Contact. Create a Contact form on the Contact route with inputs for Name,
> Email, and Message. Add client-side validation to ensure email format is
> valid and fields aren't empty. Set up Vitest and React Testing Library.
> Write 3 unit tests testing component rendering and form validation. Create a
> `prompts.md` file in the root directory and log all the prompts we used so
> far to scaffold and build this app.

**Result:** (this entry — see commits/diffs in `Week1/` for the implementation)
- Installed `react-router-dom`; added `Layout` component with a `Navbar` and
  `<Outlet />`, and `Home`, `About`, `Contact` route pages.
- Built a `Contact` form (Name, Email, Message) with client-side validation:
  required-field checks and an email-format regex check, inline error
  messages, and a success state on valid submit.
- Installed `vitest`, `@testing-library/react`, `@testing-library/jest-dom`,
  `@testing-library/user-event`, and `jsdom`; configured Vitest in
  `vite.config.js` and added a test setup file.
- Wrote 3 unit tests: Navbar renders a link for each route (component
  rendering), Contact form shows errors for empty fields + invalid email
  format (form validation), and Contact form submits successfully and shows a
  success message with valid input (form validation).
- Verified everything manually in a running dev server (browser walkthrough
  of Home → About → Contact, empty submit, invalid-email submit, valid
  submit) in addition to `npm run lint`, `npm run test`, and `npm run build`
  all passing.
- Removed `src/assets/hero.png` and `public/icons.svg`, leftover boilerplate
  assets no longer referenced after replacing the default Vite/React landing
  page with the Home/About/Contact routes.

---

### 4. Modernize the visual design

**Prompt:**
> make it modern design interactive through which my instructor impress
> because you are claude it is best for coding be a professional frontend
> designer

**Result:** Full visual redesign on top of the existing routing/form/test
structure, without changing app behavior the tests depend on:
- Added a light/dark theme system (CSS custom properties in `index.css`,
  `ThemeToggle` component, persisted to `localStorage`, applied before paint
  via an inline script in `index.html` to avoid a flash of the wrong theme).
- Redesigned `Navbar` into a sticky, blurred-glass header with an animated
  active-link pill, a brand mark, an animated hamburger menu for mobile
  (`<720px`), and the theme toggle — all as one set of nav links (no
  duplicated DOM) so the existing Navbar test keeps working unmodified.
- Added a `Reveal` component + `useReveal` scroll-animation hook
  (`IntersectionObserver`-based, with a safe fallback) used to fade/slide
  content in on Home's feature cards and About's timeline.
- Rebuilt `Home` with a gradient hero, decorative blurred glow, and a
  3-card feature grid; rebuilt `About` with a connected timeline of the
  build steps and a tech-stack chip row; rebuilt `Contact` with icon-prefixed
  inputs, a focus glow, shake-on-error, a loading-spinner submit state, and
  an animated success card.
- Added a `Footer`, page-transition fade on route change (`Layout`), and
  removed the now-unused `App.css` (styles moved into per-component CSS
  files).

**Correction applied (lint):** `eslint-plugin-react`'s `recommended` ruleset
enables `react/prop-types`, which would flag every new component
(`Reveal`, `Footer`, etc.) for missing PropTypes even though this project
uses plain JS with no PropTypes/TypeScript. Turned the rule off in
`eslint.config.js` rather than adding an unused dependency.

**Correction applied (test failure):** After adding `ThemeToggle`, running
`npm run test` failed with `TypeError: window.matchMedia is not a function`
— jsdom (the test environment) doesn't implement `matchMedia`. Added a small
polyfill to `src/test/setup.js` so `ThemeToggle` can read the system color
scheme preference in tests.

**Correction applied (button text vs. tests):** The submit button's
accessible name changed from "Send" to "Send message". Updated
`Contact.test.jsx` to query `getByRole('button', { name: /send/i })` instead
of an exact string match, so the test is resilient to future copy tweaks.

**Verification:** `npm run lint`, `npm run format:check`, `npm run test`
(3/3 passing), and `npm run build` all pass. Manually walked through Home →
About → Contact in a running dev server, toggled dark mode, submitted the
contact form with empty/invalid/valid data, and inspected the mobile
hamburger menu's ARIA state and CSS rules directly via DevTools-style
inspection (the sandboxed browser preview used for this session doesn't
composite frames for screenshots, so visual confirmation relied on DOM/CSSOM
inspection rather than a rendered screenshot).

---

## 2026-07-30

### 5. Move the app to the repo root and start the branch/PR workflow

**Prompt:**
> now what I want that I delete week1 folder and move all the files in
> Aribisoft root folder and then I will commit and push on main branch then
> I will create new branch named week2 ... Now you move all files like I
> said then tell me other steps for week 2 and PR etc and make confirm that
> my first week code is running

**Result:** Moved every file out of `Week1/` up to the repo root (this is one
evolving full-stack app across the internship weeks, not separate per-week
folders) and deleted the now-empty `Week1/` directory. Updated
`.claude/launch.json` and `CLAUDE.md`, which both still referenced the old
`Week1/` path. Verified the app still worked after the move
(`npm run lint`, `npm run test` — 3/3 passing, `npm run build`, and a live
`npm run dev` boot returning HTTP 200) before committing. Committed the
restructure + full Week 1 deliverable to `main` and pushed. Created a
`week2` branch off the updated `main` and pushed it, ready for Week 2's work
and a future PR back into `main`.

### 6. Scaffold the Week 2 FastAPI backend

**Prompt:**
> I am starting Week 2: Backend, REST, CRUD & ORM of the Arbisoft
> Internship. Please perform the following steps: Create a git branch named
> week2 off of main. Scaffold a clean backend folder structure inside a
> backend/ directory at the root (e.g., backend/app/main.py,
> backend/app/database.py, backend/app/models/, backend/app/schemas/,
> backend/app/routers/). Create a requirements.txt containing fastapi,
> uvicorn, sqlalchemy, pydantic, ruff, pytest, httpx. Configure Ruff for
> linting (create pyproject.toml or ruff.toml). Create a basic FastAPI entry
> point in backend/app/main.py with a /health endpoint and CORS enabled so
> our React frontend can connect later. Update prompts.md in the root
> directory logging this prompt and actions taken.

**Result:** The `week2` branch already existed from the previous prompt, so
no new branch was needed. Scaffolded:
- `backend/app/` with `main.py`, `database.py`, and empty `models/`,
  `schemas/`, `routers/` packages (each with `__init__.py`).
- `backend/app/database.py`: SQLAlchemy engine + `SessionLocal` +
  declarative `Base`, defaulting to a local SQLite file
  (`sqlite:///./app.db`) but overridable via a `DATABASE_URL` env var.
- `backend/app/main.py`: FastAPI app with `CORSMiddleware` allowing
  `http://localhost:5173` / `:5174` (the Vite dev server), and a `GET
  /health` endpoint returning `{"status": "ok"}`.
- `backend/requirements.txt`: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`,
  `ruff`, `pytest`, `httpx`.
- `backend/pyproject.toml`: Ruff config (`line-length = 100`,
  `target-version = "py312"`, rule sets `E, F, I, UP, B`, first-party import
  recognized as `app`).
- `backend/tests/__init__.py`: empty test package, ready for the CRUD/API
  tests due later this week.
- Extended the root `.gitignore` with Python-specific entries
  (`backend/.venv`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `*.db`) —
  the existing `.gitignore` was Node-only.

**Verification:** Created a venv (`backend/.venv`), installed
`requirements.txt`, ran `ruff check .` (clean), started the app with
`uvicorn app.main:app --port 8000`, and confirmed `GET /health` returns
`{"status":"ok"}` and an `OPTIONS` CORS preflight from
`Origin: http://localhost:5173` returns `200`. Confirmed via `git add -A
--dry-run` that `.venv`/`__pycache__` are correctly excluded before
committing.
