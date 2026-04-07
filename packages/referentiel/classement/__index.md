# Plan de classement

> Partie du [Référentiel de gestion documentaire](../_index.md) — v0

---

## Principe directeur

L'arborescence est organisée par **fonction métier et comptable**, pas par client ni par date.

Pourquoi ce choix :

- Un classement **par client** est intuitif au départ, mais il explose dès que tu as 20+ clients. Tu te retrouves avec des dizaines de dossiers au même niveau, sans cohérence entre eux.
- Un classement **par date** ne dit rien sur la nature du document. "2026-03" ne t'indique pas si tu cherches une facture, un contrat ou un relevé bancaire.
- Un classement **par fonction** reste stable même quand ton activité grandit. Les grandes catégories (ventes, achats, fiscalité…) ne changent pas.

---

## Les 7 dossiers racine

Ces dossiers se placent à la racine de ton espace de stockage (Drive, OneDrive, serveur, NAS). Leurs noms suivent la convention [français lisible](../regles-nommage.md#dossiers-de-larborescence) (majuscule initiale, espaces, accents).


| Dossier                                                      | Rôle                          | Contenu type                                                   |
| ------------------------------------------------------------ | ----------------------------- | -------------------------------------------------------------- |
| `[Mes ventes/](mes_ventes.md)`                               | Relation commerciale sortante | Factures clients, modèles de contrat, devis et offre, offres clients, suivi client |
| `[Mes achats/](mes_achats.md)`                               | Relation commerciale entrante | Factures fournisseurs, suivi fournisseurs                      |
| `[Mon juridique/](mon_juridique.md)`                         | Entité juridique              | Statuts, K-bis, PV d'assemblée                                 |
| `[Mon social/](mon_social.md)`                               | Gestion du personnel          | Fiches de paie, DPAE, modèles de contrat de travail, suivi salarié |
| `[Ma fiscalité/](ma_fiscalite.md)`                           | Obligations fiscales          | Déclarations TVA, liasses fiscales, avis d'imposition, avis de CFE |
| `[Ma banque et caisse/](ma_banque_et_caisse.md)`             | Trésorerie                    | Relevés bancaires                                              |
| `[Archives/](archives.md)`                                   | Années closes                 | Archives annuelles compressées avec manifest                   |


**Logique de nommage :** chaque dossier racine commence par `Mon`, `Ma` ou `Mes` (sauf `Archives/`). Le préfixe rappelle que ces documents t'appartiennent et crée une cohérence visuelle dans l'explorateur.

---

## Dossiers à volume modéré

`Mon juridique/`, `Ma banque et caisse/` utilisent une structure plate (pas de sous-dossiers mensuels) car le volume de documents reste faible.

`Mon social/` et `Ma fiscalité/` combinent des sous-dossiers chronologiques pour les documents récurrents (fiches de paie, déclarations de TVA) et une structure plate pour le reste.

Le détail de chaque arborescence est dans les pages dédiées ci-dessus.

---

## Quand adapter ce plan

Ce plan de classement est conçu pour la majorité des TPE et indépendants, mais il n'est pas universel.


| Situation                            | Adaptation                                                                              |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| Plusieurs sociétés                   | Un dossier racine par entité juridique, chacun avec cette même structure                |
| Projets longs (BTP, conseil, agence) | Ajouter un dossier `Mes projets/` avec un sous-dossier par projet                       |
| Pas de salariés                      | `Mon social/` peut être réduit à la gestion de ta propre rémunération (TNS, dividendes) |
| Activité sans devis formels          | Simplifier `Mes ventes/` en retirant `Mes modèles de devis/`, `Devis/` et `Offres/` des clients |


