---
id: M-1
type: Milestone
title: Erste lauffähige Version — Chatraum an Assistent
status: offen
tags: [durchstich, chat]
created: 2026-07-23
---

# M-1 — Erste lauffähige Version

Das Repo ist bisher **Gerüst**: Struktur, Lizenz, CI, Hygiene stehen — die Anwendung nicht.

**Fertig, wenn:** eine Nachricht aus einem Chatraum beim Assistenten ankommt, die Antwort
zurückfindet, und der Bot sich nicht selbst antwortet.

Der letzte Punkt ist kein Detail: Eine Rückkopplungsschleife zwischen Bot und eigenem Webhook
erzeugt eine Endlosschleife, die man erst an der Rechnung bemerkt.
