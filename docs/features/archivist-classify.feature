Feature: Proposer un classement LLM pour les documents de réception

Pour permettre à l'utilisateur de déterminer où ranger automatiquement les documents
déposés dans son archive, la commande classify lit les fichiers de "_Réception", extrait
leur contenu, puis interroge un LLM pour déterminer le bon dossier et construire le nom
de fichier selon les conventions du référentiel. La commande émet les décisions en JSON
sur stdout sans déplacer aucun fichier — le déplacement physique est confié à la commande
apply. Sans LLM configuré, tous les fichiers sont déclarés non classés. Une erreur sur un
fichier n'interrompt pas le traitement des autres.

Background:
  Given l'outil archivist est installé
  And un référentiel contenant une entrée "role: reception" pointant vers "_Réception"
  And un dossier "_Réception" existe dans l'archive cible

Scenario: Classification nominale — event classified avec dest_uri, fichier non déplacé
  Given un dossier "_Réception" contenant le fichier "facture.pdf"
  And le référentiel contient une entrée "Mes factures fournisseurs" avec un pattern de nommage
  And le LLM identifie l'entrée et extrait les champs date, fournisseur, numéro
  When l'utilisateur exécute "archivist classify --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "classified"
  And la ligne JSON contient "entry_id", "dest_name" et "dest_uri"
  And "dest_name" respecte le pattern de nommage défini dans le référentiel
  And le fichier "facture.pdf" est toujours présent dans "_Réception"
  And la dernière ligne stdout est un résumé JSON avec "scanned": 1, "classified": 1, "unclassified": 0, "failed": 0
  And le code de retour est 0

Scenario: LLM incertain — event unclassified, fichier non déplacé
  Given un dossier "_Réception" contenant "document_inconnu.pdf"
  And le LLM retourne "entry_id": null avec une raison d'incertitude
  When l'utilisateur exécute "archivist classify --referentiel ... --root ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "unclassified"
  And la ligne JSON contient "reason" commençant par "llm_uncertain:"
  And le fichier "document_inconnu.pdf" est toujours présent dans "_Réception"
  And le résumé final contient "unclassified": 1
  And le code de retour est 0

Scenario: Sans LLM configuré — tous les fichiers déclarés non classés
  Given un dossier "_Réception" contenant 2 fichiers
  And aucun LLM n'est configuré (ni --llm ni config)
  When l'utilisateur exécute "archivist classify --referentiel ... --root ..."
  Then le code de retour est 0
  And chaque ligne JSON contient "status": "unclassified"
  And le résumé final contient "classified": 0, "unclassified": 2
  And les fichiers sont toujours présents dans "_Réception"

Scenario: Erreur d'extraction de métadonnées — event failed, fichier non déplacé
  Given un dossier "_Réception" contenant "corrompu.pdf"
  And l'extracteur de métadonnées échoue sur ce fichier
  When l'utilisateur exécute "archivist classify --referentiel ... --root ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "failed"
  And la ligne JSON contient "reason" commençant par "metadata_error:"
  And le fichier "corrompu.pdf" est toujours présent dans "_Réception"

Scenario: Erreur LLM — event failed, fichier non déplacé
  Given un dossier "_Réception" contenant "facture.pdf"
  And le LLM échoue (timeout ou sortie non JSON)
  When l'utilisateur exécute "archivist classify --referentiel ... --root ... --llm claude-cli"
  Then la sortie stdout contient une ligne JSON avec "status": "failed"
  And la ligne JSON contient "reason" commençant par "llm_error:"
  And le fichier "facture.pdf" est toujours présent dans "_Réception"

Scenario: Traitement best-effort — une erreur n'arrête pas les autres fichiers
  Given un dossier "_Réception" contenant "corrompu.pdf" et "facture.pdf"
  And l'extracteur échoue uniquement sur "corrompu.pdf"
  And le LLM classifie correctement "facture.pdf"
  When l'utilisateur exécute "archivist classify --referentiel ... --root ... --llm claude-cli"
  Then la sortie stdout contient deux lignes JSON, une par fichier
  And le résumé final contient "scanned": 2, "classified": 1, "failed": 1
  And les deux fichiers sont toujours présents dans "_Réception"

Scenario: _Réception vide — aucun événement, résumé à zéro
  Given un dossier "_Réception" vide
  When l'utilisateur exécute "archivist classify --referentiel ... --root ... --llm claude-cli"
  Then la sortie stdout contient uniquement la ligne de résumé JSON
  And le résumé contient "scanned": 0, "classified": 0, "unclassified": 0, "failed": 0
  And le code de retour est 0

Scenario: Option --referentiel manquante
  When l'utilisateur exécute "archivist classify --root file:///path/to/archive --llm claude-cli"
  Then le code de retour est 2
  And la sortie stderr contient un message mentionnant "--referentiel"

Scenario: URI avec schéma invalide
  When l'utilisateur exécute "archivist classify --referentiel /chemin/sans/scheme --root file:///path/to/archive --llm claude-cli"
  Then le code de retour est 2

Scenario: Dossier _Réception absent de l'archive cible
  Given une archive cible sans dossier "_Réception"
  When l'utilisateur exécute "archivist classify --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive --llm claude-cli"
  Then le code de retour est 2
  And la sortie stderr contient "scaffold" dans le message d'erreur
