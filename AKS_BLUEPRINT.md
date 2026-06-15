# AKS — Reflections
### Local AI Memory System | Project Blueprint

---

## The Problem

Every AI session starts blank. You explain the same context over and over. The AI hallucinates things you already fixed, re-does work that's done, forgets decisions you made. This wastes hours.

## The Solution

A local JSON file per project that stores the real truth of your work. You feed it to any AI — Claude, ChatGPT, Gemini — and it instantly knows where you are. No cloud. No account. No prompt tricks. Just honest memory.

---

## How It Works (Simple Version)

```
Your Project Folder/
├── aks.json          ← the memory file
├── aks.py            ← the tool to update it
└── your code...
```

That's it. One JSON file. One Python script.

---

## The JSON Structure (aks.json)

```json
{
  "project_name": "my-app",
  "last_updated": "2026-06-15T02:00:00Z",
  "what_is_built": [
    "Login page with email and password",
    "Dashboard layout with sidebar"
  ],
  "in_progress": [
    "Connecting dashboard to backend API"
  ],
  "decisions_made": [
    "Using SQLite not PostgreSQL — simpler for now",
    "No user roles yet — single user only"
  ],
  "bugs_fixed": [
    "Token loop bug on login page — fixed by clearing localStorage"
  ],
  "do_not_touch": [
    "api/routes folder — structure is final"
  ],
  "next_task": "Connect dashboard stats to real data from /api/summary"
}
```

---

## The Script (aks.py) — 5 Commands

```
python aks.py init              → creates aks.json for this project
python aks.py done "built X"    → adds to what_is_built
python aks.py next "do Y"       → sets the next task
python aks.py bug "fixed Z"     → logs a bug fix
python aks.py dump              → prints context you paste into any AI
```

### The "dump" output looks like this:

```
=== AKS REFLECTION — my-app ===
Last updated: 2026-06-15

WHAT IS BUILT:
- Login page with email and password
- Dashboard layout with sidebar

IN PROGRESS:
- Connecting dashboard to backend API

DECISIONS MADE:
- Using SQLite not PostgreSQL
- No user roles yet

BUGS FIXED:
- Token loop bug on login — fixed by clearing localStorage

DO NOT TOUCH:
- api/routes folder

NEXT TASK:
- Connect dashboard stats to real data from /api/summary

=== END OF REFLECTION ===
Paste this at the start of any AI chat to restore full context.
```

---

## What We Are NOT Building

- No file watcher (no background processes)
- No automatic injection into AI
- No cloud sync
- No account or login
- No prompt manipulation

You stay in control. You run the commands. You paste the dump. Simple.

---

## Build Order for Claude Code

### Phase 1 — Core (Start Here)
1. `aks.py` — the CLI script with all 5 commands
2. `aks.json` — created by `init` command
3. Test all 5 commands work correctly

### Phase 2 — Polish
4. Add `python aks.py status` — pretty prints current state in terminal
5. Add timestamps to every entry automatically
6. Handle errors gracefully (what if aks.json is missing, corrupted, etc.)

### Phase 3 — Optional Later
7. Simple web UI to view/edit aks.json in browser (local only)
8. `aks.py export` — saves a markdown version of the reflection

---

## Tech Stack

- **Python 3** — just the standard library, no installs needed
- **JSON** — for storage
- **argparse** — for CLI commands (built into Python)

Zero dependencies. Runs anywhere Python runs.

---

## Instructions for Claude Code

Paste this into Claude Code to start:

```
Read AKS_BLUEPRINT.md. Build Phase 1:
- aks.py with commands: init, done, next, bug, dump
- Use Python standard library only, no pip installs
- aks.json should be created in whatever folder you run aks.py from
- dump command should print clean text ready to paste into any AI chat
```

---

*Built to solve a real problem. Keep it simple.*
