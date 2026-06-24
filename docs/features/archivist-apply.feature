Feature: Appliquer les décisions de classement et déplacer les fichiers

Pour permettre à l'utilisateur de finaliser le rangement automatique de ses documents,
la commande apply lit un fichier manifeste JSON produit par classify et déplace chaque
fichier de "_Réception" vers sa destination définitive. Les fichiers classifiés rejoignent
leur dossier cible ; les fichiers non classés ou en erreur sont déplacés dans "_Non classé".
Si un fichier source est absent (état périmé), il est signalé comme skipped sans erreur,
ce qui rend apply idempotent. La commande retourne un code d'erreur uniquement si des
déplacements ont échoué.

Background:
  Given l'outil archivist est installé
  And un référentiel contenant une entrée "role: non_classe" pointant vers "_Non classé"
  And le dossier "_Non classé" existe dans l'archive cible

Scenario: Déplacement nominal d'un fichier classifié
  Given un fichier "_Réception/facture.pdf" présent dans l'archive
  And un manifeste JSON contenant {"uri": ".../facture.pdf", "status": "classified", "dest_uri": ".../Factures/2026-03/2026-03_Facture_OVH.pdf"}
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then la sortie stdout contient une ligne JSON avec "status": "moved" et "dest_uri"
  And "facture.pdf" est présent dans ".../Factures/2026-03/"
  And "facture.pdf" n'est plus présent dans "_Réception"
  And le résumé final contient "moved": 1, "skipped": 0, "failed": 0
  And le code de retour est 0

Scenario: Fichier non classé — déplacé dans _Non classé
  Given un fichier "_Réception/inconnu.pdf" présent dans l'archive
  And un manifeste JSON contenant {"uri": ".../inconnu.pdf", "status": "unclassified"}
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then la sortie stdout contient une ligne JSON avec "status": "moved"
  And "inconnu.pdf" est présent dans "_Non classé"
  And "inconnu.pdf" n'est plus présent dans "_Réception"
  And le code de retour est 0

Scenario: Fichier en erreur de classification — déplacé dans _Non classé
  Given un fichier "_Réception/corrompu.pdf" présent dans l'archive
  And un manifeste JSON contenant {"uri": ".../corrompu.pdf", "status": "failed", "reason": "metadata_error"}
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then "corrompu.pdf" est déplacé dans "_Non classé"
  And le code de retour est 0

Scenario: Fichier source absent (état périmé) — événement skipped sans erreur
  Given un manifeste JSON référençant "_Réception/already_moved.pdf"
  And ce fichier n'existe plus dans "_Réception"
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then la sortie stdout contient une ligne JSON avec "status": "skipped" et "reason": "source_not_found"
  And le résumé final contient "skipped": 1, "failed": 0
  And le code de retour est 0

Scenario: Mélange de statuts — traitement best-effort
  Given 3 fichiers dans "_Réception" : "facture.pdf" (classifié), "inconnu.pdf" (non classé), "parti.pdf" (absent)
  And un manifeste correspondant aux 3 fichiers
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then le résumé final contient "moved": 2, "skipped": 1, "failed": 0
  And le code de retour est 0

Scenario: Ligne summary du manifeste ignorée silencieusement
  Given un manifeste contenant la ligne de résumé {"scanned": 1, "classified": 1} avant les événements
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then la ligne summary est ignorée sans provoquer d'erreur

Scenario: Déplacement impossible — événement failed, code de retour 1
  Given un fichier "_Réception/facture.pdf" présent dans l'archive
  And un manifeste avec "status": "classified" et "dest_uri" valide
  And le système de fichiers refuse le déplacement
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then la sortie stdout contient une ligne JSON avec "status": "failed"
  And le résumé final contient "failed": 1
  And le code de retour est 1

Scenario: Option --manifest manquante
  When l'utilisateur exécute "archivist apply --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then le code de retour est 2

Scenario: Option --referentiel manquante
  When l'utilisateur exécute "archivist apply --manifest decisions.json --root file:///path/to/archive"
  Then le code de retour est 2
  And la sortie stderr contient un message mentionnant "--referentiel"

Scenario: Dossier _Non classé absent de l'archive cible
  Given une archive cible sans dossier "_Non classé"
  When l'utilisateur exécute "archivist apply --manifest decisions.json --referentiel ... --root ..."
  Then le code de retour est 2
  And la sortie stderr contient "scaffold" dans le message d'erreur
