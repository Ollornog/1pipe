#!/usr/bin/env bash
# Das Tor vor jedem Push: die Test-Suiten.
#
#   scripts/check.sh            # alles
#   scripts/check.sh --fast     # ohne Browser-Test (kurze Schleife)
#
# Der pre-push-Hook (.githooks/pre-push) ruft dieses Skript. Einmalig pro Klon:
#   git config core.hooksPath .githooks
#
# Solange nur das Gerüst steht, ist das die Hygiene-Suite; weitere Suiten kommen mit
# dem Anwendungscode. Die Tests sind stdlib-only und brauchen kein Netz.
set -euo pipefail

cd "$(dirname "$0")/.."
FAST=0
[[ "${1:-}" == "--fast" ]] && FAST=1

step() { printf '\n\033[1m▸ %s\033[0m\n' "$1"; }
fail() { printf '\n\033[31m✗ %s\033[0m\n' "$1" >&2; exit 1; }

PY="${PYTHON:-$(command -v python3 || true)}"
[[ -n "$PY" && -x "$PY" ]] || fail "Kein python3 gefunden."
# Die Zeile ist der BELEG fuer `ci-local --matrix`: der Laeufer liest sie zurueck und
# vergleicht die Versionsnummer mit dem angeforderten Bein. Bis 2026-09-22 stand hier
# nur `sys.executable` — ein Pfad wie /opt/venvs/py313/bin/python nennt keine Version,
# und die Matrix lief deshalb in diesem Repo NIE durch ("unbelegt", Exit 1). Die
# Version gehoert also zuerst, der Pfad bleibt daneben stehen (er verraet das venv).
step "Interpreter: $("$PY" -c 'import sys; print(sys.version.split()[0], "@", sys.executable)')"

if [[ $FAST -eq 1 ]]; then
    step "Suiten (--fast)"
    "$PY" tests/run_all.py --no-browser || fail "Testsuite"
else
    step "Alle Suiten"
    "$PY" tests/run_all.py || fail "Testsuite"
fi

printf '\n\033[32m✓ Alles grün\033[0m\n'
