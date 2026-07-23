---
id: T-1
type: Task
title: Loop-Schutz — der Bot darf nicht auf sich selbst antworten
status: offen
milestone: M-1
tags: [chat, robustheit]
created: 2026-07-23
---

# T-1 — Loop-Schutz

Eingehende Nachrichten müssen erkennbar machen, ob sie vom Bot selbst stammen. Ohne diesen Schutz
löst die erste eigene Antwort den nächsten Aufruf aus.

**Fertig, wenn:** ein Test die Selbstantwort einspeist und nachweist, dass keine zweite Anfrage
entsteht — nicht nur, dass „es im Betrieb bisher nicht passiert ist".
