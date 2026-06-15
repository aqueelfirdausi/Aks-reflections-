# AKS Reflections

**Local AI memory system for your projects**

AKS Reflections keeps a living `reflections.json` in each project folder, tracking what's been built, what's in progress, decisions made, bugs fixed, and what comes next. Run `dump` at any time to get a paste-ready context block for any AI chat — no cloud, no accounts, no pip install. One Python file.

---

## Installation

Download `aks_reflections.py` and drop it in your project folder or anywhere on your PATH.

**Requirements:** Python 3.7+ — zero dependencies.

```bash
# Optional: enables dump --copy
pip install pyperclip
```

## Setup

```bash
# In your project folder:
python aks_reflections.py init
# → Initialized reflections.json for project: my-app
# → Registered in global projects list.
```

That creates `reflections.json` and registers the project in `~/.aks-reflections/projects.json`. Add `reflections.json` to your `.gitignore`.

---

## Command Reference

| Command | Description |
|---|---|
| `init [name]` | Create `reflections.json`, register project |
| `done <text>` | Log something finished (What is Built) |
| `bug <text>` | Log a bug fix |
| `inprogress <text>` | Log something in progress |
| `decision <text>` | Log a decision made |
| `donttouch <text>` | Mark something as do not touch |
| `next <text>` | Set the next task (replaces previous) |
| `undo` | Remove the most recently added entry |
| `rename <name>` | Rename project, syncs registry |
| `status` | Pretty-print all sections in terminal |
| `dump [--copy]` | Print AI-ready context block, optionally copy |
| `export [path]` | Save project as a Markdown file |
| `search <query>` | Case-insensitive search across all sections |
| `clear <section>` | Clear one section |
| `clear --all --confirm` | Wipe all sections |
| `serve` | Open live web dashboard in browser |
| `projects` | List all registered projects |
| `register` | Register current folder in global list |
| `unregister` | Remove current folder from global list |
| `switch <name>` | Print path to a registered project |

---

## Examples

### Logging work

```bash
python aks_reflections.py done "added JWT auth"
# Logged as built: added JWT auth

python aks_reflections.py bug "fixed null pointer on empty config"
# Bug fix logged: fixed null pointer on empty config

python aks_reflections.py inprogress "refactoring the data layer"
# Logged as in progress: refactoring the data layer

python aks_reflections.py decision "use postgres over sqlite for multi-user support"
# Decision logged: use postgres over sqlite for multi-user support

python aks_reflections.py donttouch "SECTION_MAP — clear and search depend on this"
# Logged as do not touch: SECTION_MAP — clear and search depend on this

python aks_reflections.py next "add pagination to project list"
# Next task set: add pagination to project list
```

### Undoing a mistake

```bash
python aks_reflections.py done "wrong entry"
python aks_reflections.py undo
# Undone [Done]: wrong entry
```

`undo` finds the most recently added entry across all sections by timestamp and removes it. No confirmation needed — it's one step.

### Viewing status

```bash
python aks_reflections.py status
```

```
==================================================
  AKS REFLECTIONS — my-app
  Last updated: 2026-06-15 14:00 UTC
==================================================

WHAT IS BUILT  (2)
  [2026-06-15 13:45]  added JWT auth
  [2026-06-15 13:52]  fixed null pointer on empty config

IN PROGRESS  (1)
  [2026-06-15 13:58]  refactoring the data layer

NEXT TASK
  [2026-06-15 14:00]  add pagination to project list
==================================================
```

### Dumping context for AI

```bash
python aks_reflections.py dump
python aks_reflections.py dump --copy   # also copies to clipboard
```

Paste the output at the start of any AI chat to instantly restore full project context.

### Exporting to Markdown

```bash
python aks_reflections.py export                    # → reflections.md (current dir)
python aks_reflections.py export ~/docs/my-app.md  # absolute path
python aks_reflections.py export reports/week1.md  # relative path, dirs auto-created
```

### Searching entries

```bash
python aks_reflections.py search auth
# 2 results for 'auth':
#   [Done]  [2026-06-15 13:45]
#     added JWT auth
#   [Decisions Made]  [2026-06-15 13:50]
#     use postgres over sqlite for multi-user support
```

Case-insensitive. Searches all sections including Next Task.

### Clearing entries

```bash
python aks_reflections.py clear done         # clears What is Built
python aks_reflections.py clear bugs         # clears Bugs Fixed
python aks_reflections.py clear inprogress   # clears In Progress
python aks_reflections.py clear decisions    # clears Decisions Made
python aks_reflections.py clear donttouch    # clears Do Not Touch
python aks_reflections.py clear next         # clears Next Task

python aks_reflections.py clear --all                   # blocked — prints safety hint
python aks_reflections.py clear --all --confirm         # wipes everything
```

### Renaming a project

```bash
python aks_reflections.py rename "my-app-v2"
# Renamed: 'my-app' → 'my-app-v2'
```

Updates `project_name` in `reflections.json` and syncs `~/.aks-reflections/projects.json` in one step.

### Web dashboard

```bash
python aks_reflections.py serve
# AKS Reflections Dashboard  →  http://localhost:5050
```

Opens a local dashboard in the browser. Features:
- Live reload every 2.5 seconds when `reflections.json` changes
- **Done / Bug Fix / Next Task / In Progress** buttons log entries without touching the terminal
- **Copy Dump** copies the full AI context block to clipboard
- **Project switcher** dropdown to jump between all registered projects

---

## Multi-project workflow

AKS Reflections maintains a global registry at `~/.aks-reflections/projects.json`. Every `init` registers automatically. Multiple projects, one registry.

```bash
# Project A
cd ~/projects/api
python aks_reflections.py init "api"

# Project B
cd ~/projects/frontend
python aks_reflections.py init "frontend"

# List all registered projects from anywhere
python aks_reflections.py projects
```

```
==================================================
  AKS REFLECTIONS — Registered Projects
==================================================
  1. api  ◀ current
     /home/user/projects/api
  2. frontend
     /home/user/projects/frontend
==================================================
```

### Switching between projects

`switch` prints the path to any registered project by partial name match:

```bash
python aks_reflections.py switch front
# /home/user/projects/frontend
#
# To switch, run:
#   cd "/home/user/projects/frontend"
```

### Dashboard project switcher

The `serve` dashboard has a dropdown in the header — select any registered project to view and log entries for it without leaving the browser.

### Registering an existing project

If you already have a `reflections.json` from before v0.3:

```bash
python aks_reflections.py register
# Registered 'my-app' → /home/user/projects/my-app
```

### Removing a project from the registry

```bash
python aks_reflections.py unregister
# Unregistered: /home/user/projects/my-app
```

This only removes the registry entry — `reflections.json` is untouched.

---

## File layout

```
your-project/
├── aks_reflections.py   ← the whole tool, one file
└── reflections.json     ← auto-created by init (add to .gitignore)
```

Global registry:
```
~/.aks-reflections/
└── projects.json        ← shared across all projects
```
