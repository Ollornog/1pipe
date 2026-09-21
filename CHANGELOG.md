# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Das Format folgt lose
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/), die Versionen
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Geändert — Python 3.12 ist die neue Untergrenze (Matrix 3.12 / 3.13 / 3.14)

`requires-python` steigt von `>=3.10` auf `>=3.12`, die CI fährt **3.12, 3.13, 3.14** statt
3.10 / 3.12 / 3.13.

Dahinter steht keine Zahl, sondern ein Fenster: **die letzten drei stable Minors**. Python 3.10
geht am 31.10.2026 EOL — eine Version, die niemand mehr fährt, ist eine Zusage ohne Deckung.
Die Obergrenze bleibt bewusst bei 3.14: 3.15 erscheint am 01.10.2026, kommt aber erst ins Gate,
wenn sie auch wirklich gelaufen ist.

Geführt wird die Matrix jetzt an **einer** Stelle (`repokit`, `tests/_kit/python_matrix.json`);
das CI-Abbild `ci-python-web` trägt dieselben drei Interpreter.

### Hinzugefügt — Backlog im Repo (`backlog/`)

Meilensteine, Aufgaben und **Entscheidungen (ADR)** liegen als Markdown mit Frontmatter unter
`backlog/`, geprüft von der Testsuite (`python3 scripts/_backlog.py list|check|index`).
Verworfene Entscheidungen werden nicht gelöscht, sondern bekommen `status: verworfen` und
`superseded_by`.

### Geändert

- **Geteilte Testbasis auf repokit 0.7.0** (`repokit sync`): bringt `tests/_kit/headers.py` mit —
  Prüfungen für Security-Header und Cookie-Flags. 1pipe setzt derzeit keine eigenen Cookies, die
  Datei liegt für später bereit. `STANDARD_POLICY` verlangt bewusst kein HSTS: das setzt der
  Reverse-Proxy, eine App-Suite kann es gar nicht sehen.
- **Projekt in `1pipe` umbenannt** (vormals ChatWisMe): Repository, Paketname, README und
  Übersetzung, Badges, Sicherheits-/Community-Dateien und Kontaktadresse.
- **Logo** auf `docs/pipe.png` (Rohrfitting statt Mikrofon) gewechselt; zwei weitere
  Pipe-Varianten `docs/pipe-2.png`/`docs/pipe-3.png` liegen als Alternativen bei. Bildnachweis
  (Flaticon, vectorsmarket15) im README beider Sprachfassungen ergänzt.
- **Bildnachweis** verlinkt jetzt direkt die Autorenseite (statt der Flaticon-Suchseite) und
  öffnet in neuem Tab; einheitliches Format `Icon: … PNG Image by … - flaticon.com`.

## [0.1.0] - 2026-07-12

### Hinzugefügt

- **Repo-Gerüst** nach dem Bootstrap der übrigen öffentlichen Repos, noch vor dem Anwendungscode:
  MIT-Lizenz, zweisprachige Doku (Root Englisch, Übersetzungen unter `i18n/`), Verhaltenskodex,
  Sicherheitsrichtlinie, Mitwirken-Leitfaden, geteilte Testbasis (`tests/_kit/`), gehärtete CI
  (SHA-gepinnte Actions, `permissions:`, `ubuntu-latest`) und Dependabot.
- **Logo** `docs/microphone.png` im README-Kopf beider Sprachfassungen.
