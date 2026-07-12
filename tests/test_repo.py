#!/usr/bin/env python3
"""Hygiene: was man beim Aufräumen vergisst, prüft eine Maschine besser.

Pflichtdateien, Versionsgleichstand, keine Artefakte, keine Geheimnisse — und **keine
persönlichen Namen**: kein eigener Host, keine eigene Domain, kein Kundenname. Das Repo ist
öffentlich; die Regel darf nicht am Vorsatz hängen.

Solange nur das Gerüst steht, ist dies die einzige Suite. Weitere kommen mit dem Anwendungscode.
Die allgemeinen Prüfungen und die Sperrlisten stehen in `tests/_kit/` — einer geteilten,
eingecheckten Basis, die `repokit sync` hierher schreibt.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _kit import hygiene  # noqa: E402
from _kit.report import Report  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
r = Report("Hygiene — Repo")

POLICY = hygiene.lade_policy()
PROJEKTE = ["1pipe"]

DATEIEN = hygiene.getrackte_dateien(str(ROOT))


# ---- Pflichtdateien (zweisprachig, wo es den Leser betrifft)
PFLICHT = [
    "README.md", "i18n/README.de.md", "LICENSE", "CHANGELOG.md",
    "CONTRIBUTING.md", "i18n/CONTRIBUTING.de.md", "SECURITY.md", "i18n/SECURITY.de.md",
    "CODE_OF_CONDUCT.md", "i18n/CODE_OF_CONDUCT.de.md",
    "pyproject.toml", ".ci-image", ".gitignore",
    "scripts/check.sh", "scripts/_residue_check.sh", ".githooks/pre-push",
    ".github/workflows/ci.yml", ".github/dependabot.yml",
    "tests/_kit/hygiene.py", "tests/run_all.py", "docs/pipe.png",
]
fehlt = hygiene.pruefe_pflichtdateien(str(ROOT), PFLICHT)
r.check("alle Pflichtdateien vorhanden", not fehlt, " | ".join(fehlt))

# ---- Keine private Infrastruktur
# `admin@example.de` ist harmlos — `paperless.example.de` verrät, wo ein Paperless läuft.
treffer = hygiene.pruefe_private_infrastruktur(str(ROOT), DATEIEN, POLICY, PROJEKTE)
r.check(f"keine private Infrastruktur ({len(POLICY['private_muster'])} Muster"
        f" + {len(POLICY['private_namen_sha256_16'])} Namen)",
        not treffer, " | ".join(sorted(set(treffer))[:4]))

# ---- Nur neutrale Beispieladressen (img.shields.io liefert die README-Badges,
#      flaticon.com trägt den lizenzpflichtigen Bildnachweis fürs Logo)
adressen = hygiene.pruefe_adressen(str(ROOT), DATEIEN, POLICY,
                                   zusaetzliche_hosts=[r"img\.shields\.io",
                                                       r"(?:www\.)?flaticon\.com"])
r.check("nur neutrale Beispieladressen", not adressen, " | ".join(sorted(set(adressen))[:4]))

# ---- Keine Geheimnisse; Version steht überall gleich
lecks = hygiene.pruefe_geheimnisse(str(ROOT), DATEIEN, POLICY)
r.check("keine Geheimnisse im Klartext", not lecks, " | ".join(lecks[:3]))

pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
versionsfehler = hygiene.pruefe_versionsgleichstand(str(ROOT))
r.check(f"Version {version}: pyproject, CHANGELOG und SemVer stimmen",
        not versionsfehler, " | ".join(versionsfehler))

# ---- Keine Artefakte
artefakte = hygiene.pruefe_artefakte(DATEIEN, POLICY)
r.check("keine generierten Artefakte versioniert", not artefakte, " | ".join(artefakte[:3]))
r.check("keine .env versioniert", not [f for f in DATEIEN if Path(f).name == ".env"])

# ---- Belegte Standards, maschinell erzwungen (context/repo-standards.md)
ungepinnt = hygiene.pruefe_actions_sha_gepinnt(str(ROOT), DATEIEN)
r.check("Actions per Commit-SHA gepinnt, nicht per Tag", not ungepinnt, " | ".join(ungepinnt[:3]))

ohne_rechte = hygiene.pruefe_workflow_permissions(str(ROOT), DATEIEN)
r.check("jeder Workflow setzt `permissions:`", not ohne_rechte, " | ".join(ohne_rechte[:3]))

runner = hygiene.pruefe_kein_self_hosted_runner(str(ROOT), DATEIEN)
r.check("kein self-hosted Runner (öffentliches Repo)", not runner, " | ".join(runner[:3]))

kategorien = hygiene.pruefe_changelog_kategorien(str(ROOT), POLICY)
r.check("CHANGELOG nutzt gültige Kategorien", not kategorien, " | ".join(kategorien[:2]))

uebersetzung = hygiene.pruefe_uebersetzungs_struktur(str(ROOT), [("README.md", "i18n/README.de.md")])
r.check("README.de.md folgt der Struktur von README.md", not uebersetzung, " | ".join(uebersetzung[:2]))

# ---- Jede Suite läuft im Sammellauf mit
sammel = hygiene.pruefe_run_all_sammelt_automatisch(str(ROOT))
r.check("run_all.py findet die Suiten automatisch", not sammel, " | ".join(sammel))

# ---- Ausführbarkeit
nicht_x = hygiene.pruefe_ausfuehrbar(str(ROOT), ["scripts/check.sh", ".githooks/pre-push"])
r.check("scripts/check.sh und pre-push sind ausführbar", not nicht_x, " | ".join(nicht_x))

sys.exit(r.done())
