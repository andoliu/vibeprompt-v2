# -*- coding: utf-8 -*-
"""Batch 2: add v0/bolt/windsurf prompts + claude-code code-review scene (idempotent)."""
import json, io
from collections import Counter

D = '2026-09-23'
NEW = [
  {"id": "v0-001", "tool": "v0", "scene": "landing", "title": "SaaS Landing Page, shadcn Style",
   "prompt": "Build a landing page for <product>, a <one-line description> for <audience>. Use Next.js + Tailwind + shadcn/ui. Sections: sticky nav (logo, 3 links, CTA); hero with headline '<headline>', subheadline, primary and secondary CTA; logo strip; 3 feature cards with lucide icons; product screenshot placeholder in a browser frame; 3-tier pricing (middle highlighted 'Most popular'); 5-question FAQ accordion; footer with 4 columns. Dark mode support, mobile-first, subtle animations only. No lorem ipsum — write real copy.",
   "note": "v0's sweet spot: full pages with the exact component vocabulary it knows.", "date": D},
  {"id": "v0-002", "tool": "v0", "scene": "dashboard", "title": "Analytics Dashboard Skeleton",
   "prompt": "Build a dashboard page with shadcn/ui: left sidebar (collapsible, 5 nav items with icons); top bar with breadcrumb, search input and user avatar dropdown; content area with 4 stat cards (label, value, +x% trend badge); one area chart placeholder (recharts) with a 7d/30d/90d range toggle; one recent-events table with status badges and pagination. Dark mode, responsive: sidebar becomes a drawer on mobile. Fill with realistic sample data, no placeholders.",
   "note": "Structure-complete dashboard you can wire to real data after.", "date": D},
  {"id": "v0-003", "tool": "v0", "scene": "landing", "title": "Pricing Page with Toggle",
   "prompt": "Build a pricing page for <product>: monthly/yearly toggle (yearly shows '2 months free'); 3 tier cards — name, audience fit line, price, 7 feature rows with check icons, CTA (middle tier highlighted + 'Most popular' badge); comparison table with 8 rows below; 5-question pricing FAQ; trust line '14-day refund, no card required'. Use shadcn Card, Badge and Table components. Prices: <list yours>. Mobile: cards stack, table scrolls horizontally.",
   "note": "Specify real prices — v0 fills gaps with believable-looking wrong ones.", "date": D},
  {"id": "v0-004", "tool": "v0", "scene": "forms", "title": "Waitlist Form with Validation & Success State",
   "prompt": "Build a waitlist section: centered card with headline, one-line pitch, email input + submit button (shadcn Input + Button). Client-side validation (valid email required, inline error text); on submit show a success state replacing the form: check icon, 'You're #<n> on the list', and a copyable referral link (?ref=). Include a subtle 'we never spam' microcopy line. Keep it dependency-free beyond shadcn.",
   "note": "Small page, but forces v0 to handle states, not just looks.", "date": D},
  {"id": "bolt-001", "tool": "bolt", "scene": "mvp", "title": "Full-Stack CRUD MVP in One Shot",
   "prompt": "Build a full-stack <resource> tracker (e.g. expenses, tasks, clients): React frontend with list view, create/edit modal and delete confirm; Express + SQLite backend with REST CRUD endpoints; simple stats row on top (total, count, latest). Seed 5 demo rows. Run entirely in-browser, no external services. Keep files small and the code boring — this is an MVP to validate the workflow, not a portfolio piece.",
   "note": "Bolt's differentiator: the whole stack runs in one browser sandbox.", "date": D},
  {"id": "bolt-002", "tool": "bolt", "scene": "internal-tools", "title": "Admin Table with Search, Filter, Pagination",
   "prompt": "Build an internal admin page for managing <resource>: data table with search box, a status filter dropdown, column sorting, 10-per-page pagination and row count display; each row has Edit (opens a side drawer form) and Archive (with confirm). Header shows totals per status. Use mock data of 30 rows with realistic values. Prioritize desktop layout, keyboard-friendly (Enter saves, Esc cancels).",
   "note": "The internal-tool pattern every company needs and nobody wants to build.", "date": D},
  {"id": "bolt-003", "tool": "bolt", "scene": "mobile", "title": "Mobile-First PWA Starter",
   "prompt": "Build a mobile-first habit tracker PWA: bottom tab navigation (Today, Habits, Stats); Today view with checkable habit cards and a streak flame per habit; Habits view with add/edit/delete; Stats view with a simple 7-day completion bar chart. Installable (manifest + icons), works offline with local storage persistence. Dark mode default. No backend.",
   "note": "Bolt handles the manifest/service-worker plumbing well.", "date": D},
  {"id": "bolt-004", "tool": "bolt", "scene": "api", "title": "REST API Prototype with Docs Page",
   "prompt": "Build an Express REST API for <resource> with: CRUD endpoints, input validation returning proper 400s, 404 for missing ids, CORS enabled; plus a single-page docs view at '/' listing every endpoint with method, path, params, and a 'Try it' button that fires the request and shows the JSON response. Seed sample data. This prototype is for showing a client tomorrow — make error messages human-readable.",
   "note": "The docs page makes the prototype demo itself.", "date": D},
  {"id": "ws-rules-001", "tool": "windsurf", "scene": "rules", "title": "Project .windsurfrules Template",
   "prompt": "# Project Rules\n\n- Stack: <your stack — e.g. Next.js 15 + TypeScript + Tailwind + Postgres>\n- All new code must type-check and lint clean before you report done\n- Prefer editing existing files over creating new ones; never create a file without stating why\n- Tests colocated as *.test.ts, Vitest; every bug fix ships with a failing-first test\n- No new dependencies without asking; if a task seems to need one, propose it and wait\n- Commits: imperative, under 72 chars; never mix refactor and feature\n- When requirements are ambiguous, list the 2 most likely readings and pick the conservative one, noting the choice",
   "note": "Windsurf reads .windsurfrules on every Cascade interaction — set once, applies everywhere.", "date": D},
  {"id": "ws-workflow-002", "tool": "windsurf", "scene": "workflows", "title": "Cascade Feature Workflow: Plan → Build → Verify",
   "prompt": "We're building: <feature description>. Follow this workflow strictly:\nPLAN — list every file you'll touch and the order; wait for my OK.\nBUILD — one file at a time, each step must compile; stop if a step breaks something unexpected and tell me.\nVERIFY — run the full test suite plus a manual test script you write for this feature; report results honestly, including what you did NOT test.\nDo not skip PLAN even when the feature seems small.",
   "note": "Tames Cascade's tendency to sweep through 30 files in one go.", "date": D},
  {"id": "ws-refactor-003", "tool": "windsurf", "scene": "refactoring", "title": "Behavior-Preserving Refactor Pass",
   "prompt": "Refactor <file or module> with one rule above all: BEHAVIOR MUST NOT CHANGE.\nSequence: (1) list current observable behaviors as test cases and add them BEFORE touching code; (2) run them green; (3) refactor in small commits — rename, extract, dedupe — running tests after each; (4) report the diff summary and any dead code found but not deleted. If a test fails mid-refactor, stop and show me.",
   "note": "Test-first refactoring — the safe version of 'make this code better'.", "date": D},
  {"id": "ws-tests-004", "tool": "windsurf", "scene": "testing", "title": "Test Suite Bootstrapper",
   "prompt": "Bootstrap tests for <module>: (1) inventory every exported function with a one-line behavior guess; (2) for each, write happy-path + one edge case + one failure case; (3) flag any function you cannot test without mocks and propose the mock design; (4) run the suite and report coverage before/after. Tests must fail meaningfully when the code breaks — verify by temporarily breaking one thing (then restore it).",
   "note": "The 'verify tests can fail' step catches suites that pass vacuously.", "date": D},
  {"id": "cc-review-001", "tool": "claude-code", "scene": "code-review", "title": "Skeptical Senior Review",
   "prompt": "Review this diff as a skeptical senior engineer who has been paged at 3am because of 'harmless' changes. Check in order, stop at first category with findings: (1) correctness — what breaks at the boundaries: empty, null, huge, concurrent, offline; (2) failure behavior — what happens when the DB/network/dependency is down; (3) security — injection, auth bypass, secrets in logs, tenant leakage; (4) readability — names that lie, dead code. Per finding: file:line, severity (blocker/should-fix/nit), one-line problem, one-line fix. No praise, no summary.",
   "note": "Severity-ordered checklist, tuned to find what causes incidents.", "date": D},
  {"id": "cc-review-002", "tool": "claude-code", "scene": "code-review", "title": "Security-Only Pass",
   "prompt": "Security review only, this diff. Check every input path: where does user-controllable data enter, and where does it end up (query, template, shell, redirect, file path, log)? For each, name the injection class that applies and whether the existing escaping/validation actually blocks it. Also: auth checks on every new route, tenant isolation on every new query, secrets handling, error messages that leak internals. Output a table: location, risk, evidence, fix. If you find nothing in a category, say 'checked, clean' — do not pad.",
   "note": "Follows the data, not the checklist.", "date": D},
  {"id": "cc-review-003", "tool": "claude-code", "scene": "code-review", "title": "Pre-Merge Readability Pass",
   "prompt": "This diff is functionally done. Now review it for the next reader only: (1) names that mislead more than they explain; (2) comments that narrate the code instead of explaining why; (3) nesting deeper than 3 levels that could be early-returns; (4) functions doing two jobs; (5) changes unrelated to the stated purpose (should be a separate commit). Nit-level is welcome here — but every suggestion must come with the one-line rewrite.",
   "note": "The pass to run when correctness is settled and craft is the goal.", "date": D},
]

path = 'src/data/prompts.json'
prompts = json.load(io.open(path, encoding='utf-8'))
existing = {p['id'] for p in prompts}
added = [p for p in NEW if p['id'] not in existing]
prompts.extend(added)
json.dump(prompts, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('added:', len(added), '| total:', len(prompts), dict(Counter(p['tool'] for p in prompts)))
