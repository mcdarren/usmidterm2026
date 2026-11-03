"""Rebuild results.json from a dump of the Night Desk database.

Usage: python3 scripts/build_results.py <dump_dir> <output_json>

<dump_dir> holds summary/current.json, races/*.json and feed/*.json,
as written by ArtifactData reads with out_dir.
"""
import glob
import json
import os
import sys


def load(path):
    with open(path) as f:
        doc = json.load(f)
    data = dict(doc.get("data", doc))
    data["id"] = doc.get("id", os.path.basename(path)[:-5])
    return data


def main(dump_dir, out_path):
    summary = load(os.path.join(dump_dir, "summary", "current.json"))
    summary.pop("id", None)
    races = sorted((load(p) for p in glob.glob(os.path.join(dump_dir, "races", "*.json"))), key=lambda r: r["id"])
    feed = sorted((load(p) for p in glob.glob(os.path.join(dump_dir, "feed", "*.json"))), key=lambda f: str(f.get("at", "")), reverse=True)[:200]
    if not races:
        sys.exit("No races found in dump; refusing to overwrite results.json")
    with open(out_path, "w") as f:
        json.dump({"summary": summary, "races": races, "feed": feed}, f, indent=1)
    print(f"Wrote {len(races)} races and {len(feed)} feed entries to {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
