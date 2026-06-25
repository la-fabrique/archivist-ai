Feature: Persister un journal d'audit des sessions classify

Pour permettre à l'utilisateur de consulter l'historique des traitements effectués par
la commande classify, chaque exécution est enregistrée dans un fichier SQLite local.
Le journal contient les événements par document (statut, codes d'erreur, raisons LLM)
ainsi qu'un résumé de session (compteurs, timestamps, référentiel utilisé). L'écriture
du journal est non bloquante : une erreur de persistance ne fait pas échouer la commande.

Background:
  Given l'outil archivist est installé
  And un référentiel valide est disponible
  And une archive cible contenant les dossiers "_Réception", "_Conservation brut" et "_Non classé"

Scenario: Session classify persistée après traitement nominal
  Given un dossier "_Réception" contenant "facture.pdf"
  And le LLM classifie correctement le document
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then le fichier "audit.db" est créé dans le répertoire de données de l'application
  And "audit.db" contient une ligne dans la table des sessions avec "scanned": 1, "classified": 1
  And la session enregistre l'URI du référentiel utilisé
  And la session enregistre un timestamp de début antérieur au timestamp de fin
  And la session contient un identifiant unique (UUID)

Scenario: Événements détaillés enregistrés dans le journal
  Given un dossier "_Réception" contenant "facture.pdf" et "inconnu.pdf"
  And le LLM classifie "facture.pdf" correctement
  And le LLM retourne "entry_id": null pour "inconnu.pdf" avec une raison d'incertitude
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then "audit.db" contient deux événements liés à la session
  And l'événement pour "facture.pdf" a le statut "classified" et l'entry_id correspondant
  And l'événement pour "inconnu.pdf" a le statut "unclassified", "error_code": "llm_uncertain" et la raison LLM

Scenario: Erreur d'écriture audit — classify continue sans échouer
  Given un dossier "_Réception" contenant "facture.pdf"
  And le répertoire de données de l'application n'est pas accessible en écriture
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then le code de retour est 0
  And la sortie stdout contient les événements de classification normalement
  And la sortie stderr contient un avertissement mentionnant l'échec de l'audit

Scenario: Sessions successives — journal cumulatif
  Given "audit.db" existe déjà et contient une session antérieure
  And un dossier "_Réception" contenant "nouveau.pdf"
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then "audit.db" contient désormais deux sessions
  And la session antérieure est préservée intacte
  And la nouvelle session a un identifiant distinct

Scenario: Session avec _Réception vide — enregistrée avec compteurs à zéro
  Given un dossier "_Réception" vide
  When l'utilisateur exécute "archivist classify --referentiel ... --target ... --llm claude-cli"
  Then "audit.db" contient une session avec "scanned": 0, "classified": 0, "unclassified": 0, "failed": 0
  And aucun événement n'est enregistré pour cette session
