# ADR-008 : Pipeline scan en 3 phases séquentielles avec backup zip avant traitement

**Date:** 2026-05-06
**Status:** superseded — la commande scan a été supprimée ; les invariants (backup zip avant traitement, découverte par role) sont désormais portés par la commande classify

## Context

La commande `scan` traite des fichiers déposés dans `_Réception` : extraction de métadonnées puis suppression du fichier original. Sans sauvegarde préalable, une erreur en cours de traitement entraînerait une perte définitive du document original.

## Decision

Le use case `scan` suit 3 phases séquentielles strictes — (1) backup zip synchrone vers `_Conservation brut`, (2) extraction de métadonnées async, (3) suppression synchrone de `_Réception` — et les dossiers cibles sont découverts via le champ `role` du référentiel (`role: reception` / `role: conservation_brut`), pas par chemin codé en dur.

## Consequences

- Un fichier dont le backup échoue (`FilesystemError` sur `zip_file`) n'est ni extrait ni supprimé : il reste intact dans `_Réception`.
- La suppression (phase 3) a lieu même si l'extraction a échoué : l'original est toujours archivé en phase 1 avant d'être détruit.
- Le référentiel doit contenir exactement 1 entrée `role: reception` et 1 entrée `role: conservation_brut` — la commande `referentiel-cli validate` vérifie cette contrainte.
- `zip_file` et `delete_file` sont des méthodes abstraites du port `Filesystem`, couvertes par la suite de contrat `FilesystemContractSuite`.
