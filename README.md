# AKS Reflections

> Local AI memory system. Works with any AI. Zero dependencies.

---

## The Problem

Every AI session starts blank.

You explain the same project over and over. The AI hallucinates what's done, re-does work you already finished, forgets decisions you made last night. Hours wasted. Every single day.

This is not a Claude problem. Not a ChatGPT problem. Not a Gemini problem. It is every AI, every session, every time.

## The Solution

One local JSON file that holds the real truth of your project.

Run one command at the start of any session. Paste the output into any AI. It instantly knows everything — what's built, what's broken, what decisions you made, what not to touch, what's next.

No cloud. No account. No subscription. No prompt tricks. Just honest local memory you control.

---

## Works With Any AI

- Claude
- ChatGPT
- Gemini
- Grok
- Codex
- Any AI that accepts text input

---

## Install

No install. Just Python 3.

```bash
git clone https://github.com/aqueelfirdausi/Aks-reflections-.git
cd Aks-reflections-
```

That's it.

---

## Usage

### Start a new project

```bash
python aks.py init my-project
```

### Log what you built

```bash
python aks.py done "built the login page"
```

### Log a bug you fixed

```bash
python aks.py bug "fixed token loop on login — cleared localStorage"
```

### Set what's next

```bash
python aks.py next "connect dashboard to backend API"
```

### Check current state

```bash
python aks.py status
```

### Dump full context for any AI

```bash
python aks.py dump
```

Copy the output. Paste at the top of any AI chat. Done.

---

## The Dump Output

```
====== AKS REFLECTION — my-project ======
Last updated: 2026-06-15 05:30

WHAT IS BUILT:
- built the login page [2026-06-15 02:14]
- built dashboard layout [2026-06-15 03:45]

BUGS FIXED (do not repeat):
- fixed token loop on login — cleared localStorage [2026-06-15 04:10]

DECISIONS MADE:
- using SQLite not PostgreSQL

DO NOT TOUCH:
- api/routes folder

NEXT TASK:
- connect dashboard to backend API

====== END — paste above into any AI ======
```

---

## What aks.json Looks Like

```json
{
  "project_name": "my-project",
  "last_updated": "2026-06-15T05:30:00Z",
  "what_is_built": [
    { "text": "built the login page", "at": "2026-06-15 02:14" }
  ],
  "in_progress": [],
  "decisions_made": [],
  "bugs_fixed": [
    { "text": "fixed token loop on login", "at": "2026-06-15 04:10" }
  ],
  "do_not_touch": [],
  "next_task": { "text": "connect dashboard to backend API", "at": "2026-06-15 05:30" }
}
```

---

## Commands

| Command | What it does |
|---|---|
| `python aks.py init [name]` | Creates aks.json in current folder |
| `python aks.py done "text"` | Logs something you finished |
| `python aks.py bug "text"` | Logs a bug fix — AI won't repeat it |
| `python aks.py next "text"` | Sets the next task |
| `python aks.py status` | Pretty prints current project state |
| `python aks.py dump` | Prints full context ready to paste into any AI |

---

## Roadmap

- [x] v0.1 — 5 core commands, stdlib only
- [x] v0.2 — timestamps, status command, backward compat
- [ ] v0.3 — decisions and do-not-touch commands
- [ ] v0.4 — multiple dump modes (--code, --chat, --quick)
- [ ] v1.0 — web dashboard UI

---

## Why

Built by a vibe coder who got tired of AI hallucinating every night.

The memory problem is not solved by any AI lab yet. This is a simple local workaround that actually works — today, with any AI you already use.

---

## License

MIT — use it, fork it, build on it.
