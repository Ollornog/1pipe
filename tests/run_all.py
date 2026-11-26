#!/usr/bin/env python3
"""Collective run: runs every tests/test_*.py and reports a summary.

  python tests/run_all.py                # everything
  python tests/run_all.py --no-browser   # without the browser test (short loop)

Exit 0 only if every suite is green. Skipped suites are no error.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
skip_browser = "--no-browser" in sys.argv

suiten = sorted(HERE.glob("test_*.py"))
if skip_browser:
    suiten = [s for s in suiten if s.name != "test_browser.py"]

rot: list[str] = []
for suite in suiten:
    print(f"\n\033[1m▸ {suite.name}\033[0m", flush=True)
    code = subprocess.run([sys.executable, str(suite)], cwd=HERE.parent).returncode
    if code != 0:
        rot.append(suite.name)

print("\n" + "─" * 60)
if rot:
    print(f"\033[31m✗ {len(rot)} of {len(suiten)} suites red: {', '.join(rot)}\033[0m")
    sys.exit(1)
print(f"\033[32m✓ {len(suiten)} suites green\033[0m")
