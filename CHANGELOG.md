# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Das Format folgt lose
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/), die Versionen
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt — Drei neue Hygiene-Wächter (geteilte Testbasis auf repokit 0.14.0)

Alle drei schließen Lücken, die vorher **grün aussahen**:

- **Dateiliste vollständig.** `pruefe_geheimnisse([], …)` ist grün — eine leere oder
  unvollständige Dateiliste war von „alles sauber" nicht zu unterscheiden. Die Suite zählt
  jetzt gegen `git ls-tree -r HEAD` statt gegen eine Mindestzahl, weil der reale Fall nicht
  „leer" war: über `git archive` fehlte einmal das ganze `.github/`, also genau die Dateien,
  die die Workflow-Prüfungen ansehen sollen.
- **Keine blanken fremden Hostnamen.** `pruefe_adressen` sieht nur URLs **mit** Schema, das
  Muster für private Infrastruktur verlangt **drei** Namensteile — eine blanke
  Second-Level-Domain fiel durch beide. Der freigegebene Grundstock (`python.org`,
  `devguide.python.org`, `flaticon.com`) ist durchgesehen; jede **neue** Adresse wird rot.
- **`persist-credentials: false` an jedem `actions/checkout`.** Ausdrücklich **eigene
  Härtung, kein belegter Standard** — GitHub empfiehlt es nirgends. Seit `checkout@v6` liegt
  das Token in `$RUNNER_TEMP` statt in `.git/config`; es zählt dort, wo nach dem Checkout
  fremder Code läuft. Keine Ausnahme nötig: kein Job hier pusht über die git-Zugangsdaten,
  das Release läuft über `gh release create` mit `GITHUB_TOKEN`.

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
