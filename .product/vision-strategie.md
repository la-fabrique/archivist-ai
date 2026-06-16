# Archiviste IA — Vision & Stratégie

_Mise à jour : 2026-06-16 — repositionnement agent-first_

## Vision

Devenir le cerveau documentaire de référence pour l'ère des agents IA — l'expertise qu'un archiviste professionnel met des années à acquérir, disponible comme capacité dans n'importe quel assistant, pour n'importe quelle petite structure.

## Mission

Donner aux TPE et indépendants accès à une gestion documentaire de niveau expert, via un référentiel de règles visibles et un agent IA qui les applique fidèlement — sans nouvelle interface, sans formation, sans friction.

## Ambition

Rendre la gestion des documents un non-sujet pour les petites structures françaises — en faisant d'Archivist la brique documentaire standard de l'écosystème des agents IA.

## Positionnement — Agent-first

**La CLI archivist n'est pas un outil utilisateur. C'est un moteur d'agent.**

L'utilisateur final parle à son LLM (Claude, GPT, Copilot…). L'agent appelle Archivist comme un outil pour scaffolter, classifier, scanner. L'utilisateur ne voit jamais de terminal — il voit son Drive organisé.

Ce positionnement implique :
- La CLI expose des commandes claires, stables, JSON-first (stdout structuré)
- L'interface utilisateur est celle du LLM hôte
- La roadmap MCP/A2A ouvre la distribution inter-agent
- La landing parle résultats aux end-users, pas commandes

## Stratégie

**Open source comme levier de confiance et de distribution.** La CLI et le référentiel sont publiés sous licence Apache 2.0 sur [GitHub](https://github.com/la-fabrique/archivist-ai). L'open source n'est pas un sacrifice commercial : c'est le mécanisme de distribution. Les développeurs et intégrateurs d'agents peuvent l'embarquer librement ; la communauté contribue et enrichit le référentiel ; la confiance vient de la lisibilité totale du code et des règles.

**Modèle open-core à venir.** Une offre avec support dédié, SLA et accompagnement est prévue pour les organisations qui souhaitent déléguer l'opérationnel. Les détails restent à définir. Les early adopters ("fondateurs") auront un accès prioritaire.

**Référentiel ouvert comme différenciateur durable.** Le référentiel n'est pas un produit d'appel : c'est le produit. L'IA l'exécute. La confiance vient de la transparence des règles — lisibles, auditables, co-construites avec la communauté. Un LLM généraliste ne peut pas reproduire cette profondeur sans mois de travail terrain.

**Agent-first distribution.** L'intégration dans les écosystèmes LLM (MCP, tool use) permet une distribution sans app store, sans friction d'installation pour l'utilisateur final. Le développeur/intégrateur est le premier adopter ; l'end-user suit.

**Spécialisation France.** Le référentiel est ancré dans le droit fiscal français (TVA, URSSAF, CFE, durées légales de conservation). C'est une barrière à la copie et un avantage de pertinence sur les solutions généralistes.

## Objectifs actuels

| Phase | Métrique | Seuil |
|-------|----------|-------|
| MVP early access | Taux de classification correcte (dataset réel) | ≥ 85% |
| MVP early access | Inscriptions waitlist | > 200 |
| MVP early access | Coût par inscription | < 2€ |
| Post-MVP | Rétention à 30 jours (outil re-utilisé) | > 60% |
| Post-MVP | Documents classés / semaine (North Star) | croissance |

## Moyens

- **archivist-cli** — CLI Python agent-first : scaffold, classify, scan, index
- **Référentiel v0** — plan de classement, nommage, archivage (droit FR)
- **Landing page** — vitrine end-user, collecte waitlist
- **Canaux communautaires** — LinkedIn, groupes freelances/micro-entrepreneurs, forums indépendants
- **Budget ads** — 100–500€, phase conversion uniquement

## Ce qu'on ne fait PAS maintenant

- Connecteurs Drive / OneDrive natifs (roadmap)
- Recherche en langage naturel (roadmap)
- Application mobile ou UI dédiée
- Internationalisation (hors France)

