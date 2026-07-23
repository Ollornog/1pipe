---
id: ADR-1
type: Decision
title: Eigene Brücke statt allgemeines Workflow-Werkzeug
status: erledigt
tags: [architektur, ki]
created: 2026-07-12
---

# ADR-1 — Eigene Brücke statt Workflow-Werkzeug

## Kontext

Ein allgemeines Workflow-Werkzeug (Baukasten mit Knoten und visuellem Editor) kann Chat und
Sprachmodell ebenfalls verbinden. Eine solche Lösung war im Einsatz.

## Entscheidung

**Eigene, schmale Brücke.**

## Begründung

Der Baukasten ist stark, solange man in seinen Bahnen bleibt. Sobald eine Anforderung quer dazu
liegt — eigene Werkzeugaufrufe, eigene Zustandshaltung, Fehlerbehandlung mit Fachlogik — baut man
Code **im** Werkzeug, ohne dessen Vorteile zu behalten: nicht versionierbar wie Code, nicht testbar
wie Code, nicht lesbar im Diff.

## Konsequenzen

- Mehr Eigenbau, dafür eine normale Codebasis mit Tests und Changelog.
- Was der Baukasten geschenkt hätte (fertige Konnektoren), muss einzeln gebaut werden — bewusst,
  denn gebraucht wird nur eine Handvoll.
