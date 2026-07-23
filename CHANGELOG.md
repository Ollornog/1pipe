# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Das Format folgt lose
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/), die Versionen
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

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
