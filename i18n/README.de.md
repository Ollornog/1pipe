<p align="center"><img src="../docs/microphone.png" alt="ChatWisMe" width="250" height="250"></p>

<h1 align="center">ChatWisMe</h1>

<p align="center"><a href="../README.md">English</a> · <b>Deutsch</b></p>

<p align="right">
<a href="https://github.com/Ollornog/ChatWisMe/actions/workflows/ci.yml"><img src="https://github.com/Ollornog/ChatWisMe/actions/workflows/ci.yml/badge.svg" alt="tests"></a>
<a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-informational.svg" alt="License: MIT"></a>
<img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python">
</p>

### Eine schlanke, selbst gehostete KI-Chat-Plattform und ein Connector-Framework für Rocket.Chat.

ChatWisMe setzt einem Team einen Assistenten in den eigenen Chat und gibt ihm Werkzeuge: ein
Dokumentenarchiv durchsuchen, eine Todo-Liste pro Person führen, eine Web-Recherche laufen lassen.
Eine kleine Connector-Registry ordnet jedem Kanal zu, was der Assistent dort darf. Es soll ein
schwergewichtiges visuelles Automatisierungswerkzeug durch ein paar hundert Zeilen expliziten
Python ersetzen.

Gebaut mit FastAPI. Das Sprachmodell ist austauschbar; die Referenz-Verdrahtung zielt auf einen
Anbieter mit nativem Websuche-Werkzeug. Die Anmeldung ist an
[TinySesam](https://github.com/Ollornog/TinySesam) ausgelagert. Es ist ein Begleiter von
[paperlaiss](https://github.com/Ollornog/paperlaiss), das es über dessen JSON-API ansteuert, statt
es zu duplizieren.

---

## Status

**Früh — die Plattform wird gerade gebaut.** Dieses Repo trägt bislang das Projektgerüst: Lizenz,
Doku, die geteilte Testbasis und die gehärtete CI. Der Anwendungscode kommt schrittweise dahinter.
Über neue Versionen informiert der [Releases-Feed](https://github.com/Ollornog/ChatWisMe/releases);
einen `latest`-Tag gibt es bewusst nicht.

## Was es können wird

- **Einen Chat-Raum an einen Assistenten koppeln.** Ein eingehender Webhook trägt eine Nachricht
  herein; die Antwort geht über die Chat-API zurück, mit Schutz davor, dass der Bot sich selbst
  beantwortet.
- **Nach Kanal routen.** Eine Connector-Registry entscheidet, welche Werkzeuge eine Nachricht in
  einem bestimmten Kanal erreichen darf — der Dokument-Connector im einen Raum, Recherche im anderen.
- **Über Neustarts hinweg erinnern.** Das Gesprächsgedächtnis kommt aus der eigenen Historie des
  Chat-Servers, nicht aus einem getrennten Speicher, der abdriften oder bei einem Redeploy
  verschwinden kann.
- **Fragen, bevor es etwas ändert.** Verändernde Aktionen verlangen ein ausdrückliches Ja/Nein; der
  Assistent handelt nicht auf eine erschlossene Absicht hin.

## Entwurf

- **Ein Ökosystem.** Durchgängig Python und FastAPI, sodass die LLM-, Archiv- und Chat-Bausteine mit
  [paperlaiss](https://github.com/Ollornog/paperlaiss) geteilt werden — ein Deploy, ein Auth-Muster.
- **Konfiguration aus der Umgebung.** Kein Endpunkt, kein Token, kein Modell steht im Code; das Repo
  liefert nur neutrale Beispiele.
- **Auth ist ausgelagert.** Das Plattform-Panel sitzt hinter
  [TinySesam](https://github.com/Ollornog/TinySesam) und einem OIDC-Anbieter — ChatWisMe speichert
  keine Passwörter.
- **Absichtlich klein.** Ein Connector ist eine Handvoll Werkzeuge mit klarem Vertrag, kein
  Plugin-Zoo.

## Connectoren

| Connector | Was er tut |
|-----------|------------|
| **Archiv** | Dokumente in einem Paperless-ngx-Archiv suchen, öffnen und neu klassifizieren (über paperlaiss); Upload über dessen Ingest-API. |
| **Todo** | Eine Aufgabenliste pro Person, die Person an ihre Chat-/OIDC-Identität gebunden. |
| **Recherche** | Eine Web-Recherche über das Suchwerkzeug des Modells, interaktiv oder geplant, die still bleibt, wenn es nichts zu melden gibt. |

## Entwicklung

```bash
./scripts/check.sh          # Hygiene-Tests (weitere Suiten kommen mit dem App-Code)
git config core.hooksPath .githooks
```

Die Suite ist **wiederholbar**: zweimal laufen lassen muss zweimal grün sein. Siehe
[`CONTRIBUTING.de.md`](CONTRIBUTING.de.md).

## Sicherheit

Schwachstellen bitte vertraulich melden — siehe [`SECURITY.de.md`](SECURITY.de.md).

## Lizenz

[MIT](../LICENSE)
