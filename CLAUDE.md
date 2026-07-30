# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

This is a single evolving full-stack app built incrementally across an 8-week internship program (Arbisoft Internship Program 2026), not separate per-week projects — the app itself lives at the repo root (e.g. Week 3 adds auth on top of Week 2's backend on top of Week 1's frontend). Each week's work happens on its own branch and merges into `main` via PR once reviewed.

`prompts.md` at the repo root is a running log of every significant AI prompt used to build this project (a program requirement, not optional documentation) — append to it, don't replace it, when doing substantial AI-assisted work.

## Branching workflow

Work is done per-week on a branch (e.g. `week2`), pushed to GitHub, and merged into `main` via Pull Request after review — never commit or push directly to `main`. Branch off an up-to-date `main` at the start of each week's work.

## Commands (run from repo root)

```
npm run dev            # start Vite dev server
npm run build           # production build
npm run lint             # eslint .
npm run format           # prettier --write .
npm run format:check     # prettier --check .
npm run test             # vitest run (all tests)
npx vitest run src/pages/Contact.test.jsx   # single test file
npx vitest run -t "shows validation errors"  # single test by name
```

## Architecture

**Routing & layout**: `main.jsx` wraps `App` in `BrowserRouter`. `App.jsx` defines all routes nested under a single `Layout` route element (`components/Layout.jsx`), which renders `Navbar` + `Footer` around an `Outlet`. The `Outlet` is wrapped in a `div` keyed on `location.pathname` purely to retrigger the CSS fade-in animation (`page-transition` class in `Layout.css`) on every route change.

**Theming**: Light/dark theme is driven entirely by CSS custom properties in `index.css`, toggled via a `data-theme` attribute on `<html>`. `ThemeToggle.jsx` reads/writes the theme to `localStorage` (key `week1-theme`). A small inline script in `index.html` (before the app mounts) sets `data-theme` synchronously from `localStorage`/`prefers-color-scheme` to avoid a flash of the wrong theme on load.

**Scroll-reveal animation**: `hooks/useReveal.js` (IntersectionObserver, with a same-render fallback if unavailable) + `components/Reveal.jsx` (a generic wrapper accepting `as`, `className`, `delay`) is the reusable pattern for fade/slide-in-on-scroll content — used on `Home`'s feature cards and `About`'s timeline.

**Contact form validation**: Validation logic lives in `utils/validateContact.js` as a pure function (`validateContact({name, email, message}) -> errors`), kept separate from `pages/Contact.jsx` specifically so it's independently unit-testable and reusable.

**Testing**: Vitest + React Testing Library, jsdom environment (configured in `vite.config.js`). `src/test/setup.js` imports jest-dom matchers and polyfills `window.matchMedia`, which jsdom does not implement — required because `ThemeToggle` reads `matchMedia` on mount; any other code relying on `matchMedia` will need this same polyfill to be test-safe.

**ESLint**: Flat config (`eslint.config.js`) with `eslint-plugin-react` + `react-hooks` + `react-refresh`, reconciled with Prettier via `eslint-config-prettier`. `react/prop-types` is explicitly turned off (project uses plain JS, no PropTypes/TypeScript). Test files (`**/*.test.{js,jsx}`, `src/test/**`) get `globals.vitest` injected in a separate config block since `vitest.config` globals (`test`, `expect`, etc.) aren't otherwise recognized by ESLint.
