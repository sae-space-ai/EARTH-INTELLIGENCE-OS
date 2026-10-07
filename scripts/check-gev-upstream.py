#!/usr/bin/env python3
"""
Check God's Eye View upstream for updates since our pinned baseline.

Usage: python scripts/check-gev-upstream.py

This script compares our pinned baseline with the current remote upstream
and reports any changes. It does NOT automatically merge upstream code.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Pinned baseline
BASELINE = {
    "url": "https://github.com/bilawalsidhu/gods-eye-view",
    "branch": "main",
    "commit": "e685449a52550775a5279cef1b9090ef24d507a2",
    "commit_date": "2026-10-06",
    "version": "v0.2.1",
    "pinned_at": "2026-10-06",
}


def check_upstream() -> dict:
    """Check upstream repository for updates."""
    try:
        import urllib.request

        # Fetch latest commit info from GitHub API
        api_url = "https://api.github.com/repos/bilawalsidhu/gods-eye-view/commits/main"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Earth-Intelligence-OS/0.1"})

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        current = {
            "commit": data.get("sha", "unknown"),
            "commit_date": data.get("commit", {}).get("committer", {}).get("date", "unknown")[:10],
            "message": data.get("commit", {}).get("message", "").split("\n")[0],
        }

        return {
            "baseline": BASELINE,
            "current": current,
            "is_behind": current["commit"] != BASELINE["commit"],
            "checked_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "baseline": BASELINE,
            "error": str(e),
            "checked_at": datetime.utcnow().isoformat(),
        }


def main() -> int:
    """Run upstream check and report results."""
    print("=" * 60)
    print("GOD'S EYE VIEW — UPSTREAM UPDATE CHECK")
    print("=" * 60)
    print()

    result = check_upstream()

    print(f"Pinned Baseline:")
    print(f"  Commit: {result['baseline']['commit'][:12]}...")
    print(f"  Date:   {result['baseline']['commit_date']}")
    print(f"  Version: {result['baseline']['version']}")
    print()

    if "error" in result:
        print(f"⚠️  CHECK FAILED: {result['error']}")
        print()
        print("This may be due to network unavailability or rate limiting.")
        print("The pinned baseline remains valid.")
        return 1

    print(f"Current Upstream:")
    print(f"  Commit: {result['current']['commit'][:12]}...")
    print(f"  Date:   {result['current']['commit_date']}")
    print(f"  Message: {result['current']['message'][:60]}...")
    print()

    if result["is_behind"]:
        print("⚠️  UPSTREAM HAS CHANGED")
        print()
        print("The upstream repository has new commits since our baseline.")
        print("Review changes before considering any updates.")
        print()
        print("IMPORTANT: Do NOT automatically merge upstream code.")
        print("Review each change for:")
        print("  - New capabilities to port")
        print("  - License changes")
        print("  - Security fixes")
        print("  - Breaking changes")
        print()
        print(f"Baseline: {BASELINE['url']}/commit/{BASELINE['commit']}")
        print(f"Current:  {BASELINE['url']}/commit/{result['current']['commit']}")
        return 2
    else:
        print("✅ UPSTREAM IS CURRENT")
        print()
        print("Our pinned baseline matches the current upstream.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
