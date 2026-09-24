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
import subprocess  # noqa: E402
from _kit import backlog, hygiene, manifest  # noqa: E402
from _kit.report import Report  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
r = Report("Hygiene — Repo")

POLICY = hygiene.lade_policy()
PROJEKTE = ["1pipe"]

DATEIEN = hygiene.getrackte_dateien(str(ROOT))


# ---- Die gevendorte Testbasis ist unverändert
# Steht bewusst VOR allem anderen: jede folgende Prüfung kommt aus genau diesen Dateien.
# Wer hier in der Kopie nachbessert statt im Kit, schwächt den Wächter still — und genau
# das ist am 2026-09-21 passiert (derselbe Backlog-Fehler zweimal behoben, das zweite Mal
# von Hand auf main). Bis 2026-09-22 gab es die Prüfung nur als `repokit check` auf dem
# Tower; hier lief sie nie (repokit#9).
_kit_drift = manifest.pruefe(str(ROOT))
r.check(f"tests/_kit unverändert (Kit {manifest.version(str(ROOT))}; sonst: repokit sync .)",
        not _kit_drift, " | ".join(_kit_drift[:3]))

# ---- Sieht die Suite überhaupt alle Dateien? (Kit 0.14.0)
# Zweiter Wächter derselben Sorte wie der über dem Kit: dort geht es um die
# Prüffunktionen, hier um ihr Material. `pruefe_geheimnisse([], ...)` ist grün,
# und bei `ci-local` fehlten über `git archive` schon einmal genau die `.github/`-
# Dateien, die die Workflow-Prüfungen brauchen (`export-ignore` in .gitattributes).
# Deshalb wird gegen `git ls-tree -r HEAD` gezählt, nicht nur gegen eine Mindestzahl.
_liste = hygiene.pruefe_dateiliste_plausibel(DATEIEN, root=str(ROOT))
r.check(f"Dateiliste vollständig ({len(DATEIEN)} getrackte Dateien)",
        not _liste, " | ".join(_liste[:3]))

# ---- Pflichtdateien (zweisprachig, wo es den Leser betrifft)
PFLICHT = [
    "README.md", "i18n/README.de.md", "LICENSE", "CHANGELOG.md",
    "CONTRIBUTING.md", "i18n/CONTRIBUTING.de.md", "SECURITY.md", "i18n/SECURITY.de.md",
    "CODE_OF_CONDUCT.md", "i18n/CODE_OF_CONDUCT.de.md",
    "pyproject.toml", ".ci-image", ".gitignore",
    "scripts/check.sh", "scripts/_residue_check.sh", ".githooks/pre-push",
    ".github/workflows/ci.yml", ".github/dependabot.yml",
    "tests/_kit/hygiene.py", "tests/_kit/backlog.py", "tests/_kit/manifest.py",
    "scripts/_backlog.py", "backlog/README-KONVENTION.md", "tests/run_all.py", "docs/pipe.png",
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

# ---- … und keine fremden Hostnamen OHNE Schema (Kit 0.14.0)
# Die Lücke daneben: `pruefe_adressen` sieht nur URLs mit `https://`, und das Muster
# in `pruefe_private_infrastruktur` verlangt drei Namensteile. Eine blanke
# Second-Level-Domain fällt durch beide — so stand in einem öffentlichen Repo ein
# realer Firmenname.
# Der Grundstock unten ist die vom PO DURCHGESEHENE und freigegebene Liste der Hosts,
# die hier stehen dürfen (Python-Doku und der lizenzpflichtige Bildnachweis fürs Logo).
# Er ist nicht automatisch entstanden: ab jetzt wird JEDE neue Adresse rot, und sie
# kommt erst nach erneuter Durchsicht hinzu.
blank = hygiene.pruefe_blanke_adressen(str(ROOT), DATEIEN, POLICY,
                                       grundstock=["python.org", "devguide.python.org",
                                                   "flaticon.com"])
r.check("keine blanken fremden Hostnamen", not blank, " | ".join(blank[:4]))

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

# ---- Backlog: Struktur, Verweise, generierter Index
for _v in backlog.alle_pruefungen(str(ROOT)):
    r.check(f"Backlog: {_v}", False)
r.check("Backlog hat Eintraege", bool(backlog.lade(str(ROOT))))
_idx = subprocess.run([sys.executable, "scripts/_backlog.py", "index", "--dry-run"],
                      cwd=ROOT, capture_output=True, text=True)
r.check("backlog/README.md ist aktuell (sonst: scripts/_backlog.py index)", _idx.returncode == 0)

# ---- Python-Matrix: EINE Quelle, mechanisch gehalten (Kit 0.12.0, 2026-09-22)
# Bis 2026-09-22 stand die Matrix an drei Stellen — im Abbild (/opt/ci-matrix), in
# dieser ci.yml und implizit in requires-python. Gemessen am 2026-09-21 waren alle
# drei VERSCHIEDEN; jede sah für sich richtig aus, zusammen war die Zusage "wir
# testen, was wir versprechen" unbelegt. Die Quelle ist jetzt
# tests/_kit/python_matrix.json, und diese drei Prüfungen halten alles daran.
#
# Die Prüffunktionen lagen seit dem Kit-Sync in tests/_kit/, wurden aber von
# KEINEM Repo aufgerufen — gefunden beim Nachzählen am 2026-09-22. Eine Prüfung,
# die niemand ruft, ist keine.
_mx = hygiene.pruefe_python_matrix(str(ROOT), DATEIEN)
r.check("ci.yml-Matrix entspricht der geführten Python-Matrix", not _mx, " | ".join(_mx[:3]))

_rp = hygiene.pruefe_requires_python(str(ROOT))
r.check("requires-python nennt die Untergrenze der Matrix", not _rp, " | ".join(_rp[:3]))

# Die Rolling-Regel MELDET, sie ändert nichts: sonst zöge ein Python-Release die
# Flotte ungefragt mit. Sie wird erst rot, wenn das Prüfdatum in der Quelle
# verstrichen ist (naechste_pruefung) — dann ist eine Entscheidung fällig.
_rr = hygiene.pruefe_python_matrix_regel()
r.check("geführte Matrix widerspricht der Rolling-Regel nicht", not _rr, " | ".join(_rr[:3]))

# ---- cancel-in-progress darf auf dem Default-Branch nicht unbedingt greifen
# Der Schaden ist gemessen, nicht befürchtet: paperlaiss verlor am 2026-09-21 vier
# main-Läufe in 33 Sekunden, DashMyBoard drei am 2026-07-10. An einem abgebrochenen
# main-Lauf hängt hinterher kein Abbild und kein Required Check.
_cip = hygiene.pruefe_kein_abbruch_auf_default_branch(str(ROOT), DATEIEN)
r.check("kein unbedingtes cancel-in-progress auf main", not _cip, " | ".join(_cip[:3]))

# ---- Eigene Härtung, bewusst NICHT im Abschnitt "Belegte Standards" (Kit 0.14.0)
# Die Ebene gehört dazu: GitHub empfiehlt `persist-credentials: false` nirgends
# ausdrücklich (geprüft 2026-09-22 an Secure-Use-Doku und checkout-README). Seit
# checkout@v6 liegt das Token in $RUNNER_TEMP statt in `.git/config` — kleiner als die
# oft zitierte Begründung, aber nicht weg. Es zählt dort, wo nach dem Checkout
# fremder Code läuft (`tj-actions/changed-files` ist der bekannte Fall).
# Keine Ausnahme nötig: kein Job hier pusht über die git-Zugangsdaten, das Release
# läuft über `gh release create` mit GITHUB_TOKEN.
_pc = hygiene.pruefe_persist_credentials(str(ROOT), DATEIEN)
r.check("jeder actions/checkout setzt `persist-credentials: false`",
        not _pc, " | ".join(_pc[:3]))

# ---- Der Wächter über den Wächtern (repokit 0.13.0)
# Er meldet jede Kit-Prüfung, die ausgeliefert, aber nicht gerufen wird — genau der
# Fehler, der die Matrix-Prüfungen ein Jahr lang unbemerkt stillgelegt hätte.
# Ausnehmen ist erlaubt, aber nur mit Grund im Aufruf.
# ---- Die Ausnahmen und die Policy selbst werden geprüft (Kit 0.17.x)
# Beide gegen dieselbe Falle: eine Ausnahme oder ein Vorgabewert, den niemand ansieht,
# verdeckt irgendwann den nächsten echten Befund. `belegstellen` ist hier leer — dieses
# Repo hat kein Zitatverzeichnis; der Aufruf steht trotzdem, damit ein späterer Eintrag
# geprüft wird, statt still zu gelten.
_beleg = hygiene.pruefe_belegstellen_eng(str(ROOT), DATEIEN, [])
r.check("Belegstellen-Muster treffen keinen Code", not _beleg, " | ".join(_beleg[:3]))
_tab = hygiene.pruefe_tabelle_vollstaendig()
r.check("jede Kit-Prüfung steht in genau einer Liste", not _tab, " | ".join(_tab[:3]))
_pk = hygiene.pruefe_policy_schluessel_gelesen(POLICY)
r.check("jeder Policy-Schlüssel wird gelesen", not _pk, " | ".join(_pk[:3]))

# ---- Nichts wird von Dritten nachgeladen (Kit 0.18.0, PO-Regel 2026-09-23)
# Die Trennlinie: ein Link ist eine Tür, ein `src` ist ein Bote, den wir ungefragt
# losschicken. Die Ausnahmeliste ist LEER und soll es bleiben — eine Freigabe für eine
# Stelle, die man beseitigen könnte, wäre keine Ausnahme, sondern eine Billigung.
_fremd = hygiene.pruefe_keine_fremdressourcen(str(ROOT), DATEIEN, POLICY)
r.check("nichts wird von Dritten nachgeladen", not _fremd, " | ".join(_fremd[:3]))

# ---- Wird jede Testdatei überhaupt gerufen? (Kit 0.21.0)
# Von AUSSEN gefragt: ein nicht verkabelter Hygiene-Test besteht seine eigene
# Aufruf-Prüfung dadurch, dass er schweigt. Autodiscovery (run_all+glob, pytest)
# erkennt die Prüfung und schweigt dann.
_td = hygiene.pruefe_testdateien_gerufen(str(ROOT))
r.check("jede Testdatei wird von einem Läufer gerufen", not _td, " | ".join(_td[:3]))

# ---- Veröffentlichen hängt am Tag (Kit 0.21.8)
# Ein tag-getriggerter Workflow MIT `workflow_dispatch` ist der einzige, den man vor dem Tag
# prüfen kann — und genau dort lag die Falle: fünf von sechs Repos hatten den Knopf, keines
# hatte ihn je gedrückt, und ein Druck hätte aus einem BRANCH heraus veröffentlicht.
_vt = hygiene.pruefe_veroeffentlichen_am_tag(str(ROOT))
r.check("in tag-Workflows hängt jedes Veröffentlichen am Tag", not _vt, " | ".join(_vt[:3]))

_ng = hygiene.pruefe_kit_prueffunktionen_gerufen(str(ROOT))
r.check("jede Kit-Prüfung wird gerufen oder ist begründet ausgenommen",
        not _ng, " | ".join(_ng[:3]))

sys.exit(r.done())
