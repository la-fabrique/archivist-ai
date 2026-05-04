Feature: Scanner un dossier source

Pour permettre au pipeline OCR/classement de traiter des documents,
la commande scan itère les fichiers d'un dossier source et retourne
la liste structurée des fichiers trouvés, sans récursion dans les sous-dossiers.

Background:
  Given l'outil archivist est installé

Scenario: Scan nominal d'un dossier avec fichiers
  Given un dossier contenant 3 fichiers : "facture.pdf", "contrat.pdf", "releve.png"
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier"
  Then la sortie stdout est le JSON {"scanned": 3, "files": ["facture.pdf", "contrat.pdf", "releve.png"]}
  And la sortie stderr contient "INFO scanning facture.pdf"
  And la sortie stderr contient "INFO scanning contrat.pdf"
  And la sortie stderr contient "INFO scanning releve.png"
  And la sortie stderr contient "INFO scan terminé : 3 fichier(s) traité(s)"
  And le code de retour est 0

Scenario: Scan d'un dossier vide
  Given un dossier vide
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier-vide"
  Then la sortie stdout est le JSON {"scanned": 0, "files": []}
  And la sortie stderr contient "INFO scan terminé : 0 fichier(s) traité(s)"
  And le code de retour est 0

Scenario: Le scan est non récursif
  Given un dossier contenant 2 fichiers et 1 sous-dossier lui-même contenant 3 fichiers
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier"
  Then la sortie stdout liste uniquement les 2 fichiers du niveau racine
  And les fichiers du sous-dossier ne sont pas inclus

Scenario: URI avec schéma invalide
  When l'utilisateur exécute "archivist scan --source /chemin/sans/scheme"
  Then le code de retour est 2
  And la sortie stderr contient un message d'erreur sur le paramètre "--source"

Scenario: URI pointant vers un fichier plutôt qu'un dossier
  Given un fichier "document.pdf" accessible à l'URI "file:///path/to/document.pdf"
  When l'utilisateur exécute "archivist scan --source file:///path/to/document.pdf"
  Then le code de retour est 2
  And la sortie stderr contient "n'est pas un dossier valide"
