import argparse
import json
import os
import sys
from datetime import datetime, timezone

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AKS_FILE = "aks.json"


def now_ts():
    """Return current local time as a display string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def entry_text(item):
    """Extract text from an entry — handles both legacy strings and new dicts."""
    if isinstance(item, dict):
        return item.get("text", "")
    return str(item)


def entry_at(item):
    """Extract timestamp from an entry — returns empty string for legacy strings."""
    if isinstance(item, dict):
        return item.get("at", "")
    return ""


def make_entry(text):
    return {"text": text, "at": now_ts()}


def load_data():
    if not os.path.exists(AKS_FILE):
        print(f"Error: {AKS_FILE} not found. Run 'python aks.py init' first.")
        sys.exit(1)
    try:
        with open(AKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {AKS_FILE} is corrupted (invalid JSON). Fix or delete it and run init again.")
        sys.exit(1)


def save_data(data):
    data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(AKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def fmt_last_updated(raw):
    if not raw:
        return ""
    try:
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M") + " UTC"
    except ValueError:
        return raw


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_init(args):
    if os.path.exists(AKS_FILE):
        print(f"{AKS_FILE} already exists. Delete it first if you want to reinitialize.")
        sys.exit(1)

    name = args.name if args.name else os.path.basename(os.getcwd())
    data = {
        "project_name": name,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "what_is_built": [],
        "in_progress": [],
        "decisions_made": [],
        "bugs_fixed": [],
        "do_not_touch": [],
        "next_task": ""
    }
    save_data(data)
    print(f"Initialized {AKS_FILE} for project: {name}")


def cmd_done(args):
    text = args.text.strip()
    if not text:
        print("Error: description cannot be empty.")
        sys.exit(1)
    data = load_data()
    data["what_is_built"].append(make_entry(text))
    save_data(data)
    print(f"Logged as built: {text}")


def cmd_bug(args):
    text = args.text.strip()
    if not text:
        print("Error: description cannot be empty.")
        sys.exit(1)
    data = load_data()
    data["bugs_fixed"].append(make_entry(text))
    save_data(data)
    print(f"Bug fix logged: {text}")


def cmd_next(args):
    text = args.text.strip()
    if not text:
        print("Error: task description cannot be empty.")
        sys.exit(1)
    data = load_data()
    data["next_task"] = make_entry(text)
    save_data(data)
    print(f"Next task set: {text}")


def cmd_status(args):
    data = load_data()
    name = data.get("project_name", "unknown")
    updated = fmt_last_updated(data.get("last_updated", ""))
    divider = "=" * 50

    print(divider)
    print(f"  AKS STATUS — {name}")
    if updated:
        print(f"  Last updated: {updated}")
    print(divider)

    def section(title, items):
        count = len(items) if items else 0
        label = f"  ({count})" if count else ""
        print(f"\n{title}{label}")
        if not items:
            print("  (none)")
            return
        for item in items:
            at = entry_at(item)
            text = entry_text(item)
            prefix = f"  [{at}]  " if at else "  "
            print(f"{prefix}{text}")

    section("WHAT IS BUILT", data.get("what_is_built", []))
    section("IN PROGRESS", data.get("in_progress", []))
    section("DECISIONS MADE", data.get("decisions_made", []))
    section("BUGS FIXED", data.get("bugs_fixed", []))
    section("DO NOT TOUCH", data.get("do_not_touch", []))

    next_task = data.get("next_task", "")
    print("\nNEXT TASK")
    if next_task:
        at = entry_at(next_task)
        text = entry_text(next_task)
        prefix = f"  [{at}]  " if at else "  "
        print(f"{prefix}{text}")
    else:
        print("  (none)")

    print(f"\n{divider}")


def cmd_dump(args):
    data = load_data()
    name = data.get("project_name", "unknown")
    updated = fmt_last_updated(data.get("last_updated", ""))

    lines = [
        f"=== AKS REFLECTION — {name} ===",
        f"Last updated: {updated}",
        "",
    ]

    def section(title, items):
        lines.append(f"{title}:")
        if items:
            for item in items:
                text = entry_text(item)
                at = entry_at(item)
                suffix = f"  [{at}]" if at else ""
                lines.append(f"- {text}{suffix}")
        else:
            lines.append("- (none)")
        lines.append("")

    section("WHAT IS BUILT", data.get("what_is_built", []))
    section("IN PROGRESS", data.get("in_progress", []))
    section("DECISIONS MADE", data.get("decisions_made", []))
    section("BUGS FIXED", data.get("bugs_fixed", []))
    section("DO NOT TOUCH", data.get("do_not_touch", []))

    next_task = data.get("next_task", "")
    lines.append("NEXT TASK:")
    if next_task:
        text = entry_text(next_task)
        at = entry_at(next_task)
        suffix = f"  [{at}]" if at else ""
        lines.append(f"- {text}{suffix}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("=== END OF REFLECTION ===")
    lines.append("Paste this at the start of any AI chat to restore full context.")

    print("\n".join(lines))


# ── CLI wiring ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="aks",
        description="AKS — local AI memory system for your project"
    )
    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    p_init = sub.add_parser("init", help="Create aks.json for this project")
    p_init.add_argument("name", nargs="?", help="Project name (defaults to folder name)")
    p_init.set_defaults(func=cmd_init)

    p_done = sub.add_parser("done", help="Log something as built")
    p_done.add_argument("text", help="What was built")
    p_done.set_defaults(func=cmd_done)

    p_bug = sub.add_parser("bug", help="Log a bug fix")
    p_bug.add_argument("text", help="What was fixed")
    p_bug.set_defaults(func=cmd_bug)

    p_next = sub.add_parser("next", help="Set the next task")
    p_next.add_argument("text", help="What to do next")
    p_next.set_defaults(func=cmd_next)

    p_dump = sub.add_parser("dump", help="Print full context to paste into any AI")
    p_dump.set_defaults(func=cmd_dump)

    p_status = sub.add_parser("status", help="Pretty-print current project state in terminal")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
