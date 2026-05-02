# ADR-004 : Registre d'adaptateurs et versioning des ports

**Date:** 2026-05-02
**Status:** accepted

## Context

L'architecture hexagonale (ADR-001) découple les ports de leurs adaptateurs, mais ne prescrit pas comment les adaptateurs sont découverts ni comment garantir la compatibilité lors de l'évolution des contrats. Le système doit être extensible par des plugins tiers sans modifier le cœur.

## Decision

Introduire un registre centralisé (`AdapterRegistry`) qui mappe un couple `(port, nom)` vers une fabrique d'adaptateur, et doter chaque port ABC d'un attribut de classe `VERSION` entier. En v1 le registre est une table interne ; il sera étendu à la découverte par entry-points Python sans changer le reste du code.

## Consequences

- Ajouter un adaptateur interne se fait en une seule ligne dans `registry.py`, sans toucher au domain ni à l'application.
- Le contrat de fabrique (`Callable[[dict], Adapter]`) est stable dès la v1 — c'est la surface que les futurs plugins tiers consommeront.
- Un adaptateur dont le `VERSION` ne correspond pas au port est rejeté au démarrage avec un message explicite.
- Seul `registry.py` changera le jour où l'on active la découverte par entry-points.
