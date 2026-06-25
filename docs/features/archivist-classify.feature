Feature: Classifier les documents de réception via LLM

Pour permettre à l'utilisateur de ranger automatiquement les documents déposés dans
son archive, la commande classify lit les fichiers de "_Réception", sauvegarde chaque
original dans "_Conservation brut", extrait le contenu du fichier, puis interroge un
LLM pour déterminer le bon dossier et construire le nom de fichier selon les conventions
du référentiel. Les fichiers non classifiables sont déplacés dans "_Non classé". Une
erreur sur un fichier n'interrompt pas le traitement des autres.

Background:
  Given l'outil archivist est installé
  And un référentiel contenant une entrée "role: reception" pointant vers "_Réception"
  And un référentiel contenant une entrée "role: conservation_brut" pointant vers "_Conservation brut"
  And un référentiel contenant une entrée "role: non_classe" pointant vers "_Non classé"
  And les dossiers "_Réception", "_Conservation brut" et "_Non classé" existent dans l'archive cible

Scenario: Classification nominale — fichier classifié et renommé
  Given un dossier "_Réception" contenant le fichier "facture.pdf"
  And le référentiel contient une entrée "Mes factures fournisseurs" avec un pattern de nommage
  And le LLM identifie l'entrée et extrait les champs date, fournisseur, numéro
  When l'utilisateur exécute "archivist classify --referentiel file:///path/to/referentiel.yaml --target file:///path/to/archive --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "classified"
  And la ligne JSON contient "entry_id", "dest_name" et "dest_uri"
  And "dest_name" respecte le pattern de nommage défini dans le référentiel
  And le fichier est déplacé dans le dossier cible correspondant à l'entrée
  And le fichier n'est plus présent dans "_Réception"
  And "_Conservation brut" contient une archive zip du fichier original
  And la dernière ligne stdout est un résumé JSON avec "scanned": 1, "classified": 1, "unclassified": 0, "failed": 0
  And le code de retour est 0

Scenario: Classification avec organisation chronologique — sous-dossier AAAA-MM créé
  Given un dossier "_Réception" contenant "facture.pdf"
  And le référentiel contient une entrée avec "organization.type: chronological" et "subfolder_pattern: AAAA-MM"
  And le LLM extrait la date "2026-03" depuis le document
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then le fichier est déplacé dans un sous-dossier "2026-03" du dossier cible
  And le sous-dossier "2026-03" est créé s'il n'existait pas

Scenario: LLM incertain — fichier déplacé dans _Non classé
  Given un dossier "_Réception" contenant "document_inconnu.pdf"
  And le LLM retourne "entry_id": null avec une raison d'incertitude
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "unclassified"
  And la ligne JSON contient "error_code": "llm_uncertain"
  And le fichier est déplacé dans "_Non classé"
  And le fichier n'est plus présent dans "_Réception"
  And "_Conservation brut" contient une archive zip du fichier original
  And le résumé final contient "unclassified": 1

Scenario: Erreur lors du backup — fichier reste dans _Réception
  Given un dossier "_Réception" contenant "facture.pdf"
  And le système de fichiers ne peut pas créer d'archive dans "_Conservation brut"
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "failed"
  And la ligne JSON contient "error_code": "backup_error"
  And le fichier "facture.pdf" est toujours présent dans "_Réception"
  And le fichier n'est pas déplacé dans "_Non classé"
  And le résumé final contient "failed": 1
  And le code de retour est 0

Scenario: Erreur d'extraction de métadonnées — fichier déplacé dans _Non classé
  Given un dossier "_Réception" contenant "corrompu.pdf"
  And l'extracteur de métadonnées échoue sur ce fichier
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "failed"
  And la ligne JSON contient "error_code": "metadata_error"
  And le fichier est déplacé dans "_Non classé"
  And "_Conservation brut" contient une archive zip du fichier original

Scenario: Erreur LLM — fichier déplacé dans _Non classé
  Given un dossier "_Réception" contenant "facture.pdf"
  And le LLM échoue (timeout ou sortie non JSON)
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "failed"
  And la ligne JSON contient "error_code": "llm_error"
  And le fichier est déplacé dans "_Non classé"

Scenario: Traitement best-effort — une erreur n'arrête pas les autres fichiers
  Given un dossier "_Réception" contenant "corrompu.pdf" et "facture.pdf"
  And l'extracteur échoue uniquement sur "corrompu.pdf"
  And le LLM classifie correctement "facture.pdf"
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then la sortie stdout contient deux lignes JSON, une par fichier
  And le résumé final contient "scanned": 2, "classified": 1, "failed": 1
  And "facture.pdf" est classifié et déplacé dans le bon dossier
  And "corrompu.pdf" est déplacé dans "_Non classé"

Scenario: _Réception vide — aucun événement, résumé à zéro
  Given un dossier "_Réception" vide
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then la sortie stdout contient uniquement la ligne de résumé JSON
  And le résumé contient "scanned": 0, "classified": 0, "unclassified": 0, "failed": 0
  And le code de retour est 0

Scenario: Option --referentiel manquante
  When l'utilisateur exécute "archivist classify --target file:///path/to/archive --llm claude-cli"
  Then le code de retour est 2
  And la sortie stderr contient un message mentionnant "--referentiel"

Scenario: Option --llm manquante
  When l'utilisateur exécute "archivist classify --referentiel file:///path/to/referentiel.yaml --target file:///path/to/archive"
  Then le code de retour est 2
  And la sortie stderr contient un message mentionnant "--llm"

Scenario: URI avec schéma invalide
  When l'utilisateur exécute "archivist classify --referentiel /chemin/sans/scheme --target file:///path/to/archive --llm claude-cli"
  Then le code de retour est 2

Scenario: Dossier _Réception absent de l'archive cible
  Given une archive cible sans dossier "_Réception"
  When l'utilisateur exécute "archivist classify --referentiel file:///path/to/referentiel.yaml --target file:///path/to/archive --llm claude-cli"
  Then le code de retour est 2
  And la sortie stderr contient "scaffold" dans le message d'erreur

Scenario: Entrée role non_classe absente du référentiel
  Given un référentiel sans entrée "role: non_classe"
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then le code de retour est 2
  And la sortie stderr indique que le rôle "non_classe" est manquant dans le référentiel
