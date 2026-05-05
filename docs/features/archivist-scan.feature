Feature: Scanner un dossier source

Pour permettre au pipeline OCR/classement de traiter des documents,
la commande scan itère les fichiers d'un dossier source et retourne
la liste structurée des fichiers trouvés, sans récursion dans les sous-dossiers.

Background:
  Given l'outil archivist est installé

Scenario: Scan nominal d'un dossier avec fichiers
  Given un dossier contenant 3 fichiers : "facture.pdf", "contrat.pdf", "releve.png"
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier"
  Then la sortie stdout est un JSON avec "scanned": 3 et "files" contenant 3 objets avec "name", "uri", "metadata"
  And la sortie stderr contient "INFO scanning facture.pdf"
  And la sortie stderr contient "INFO scanning contrat.pdf"
  And la sortie stderr contient "INFO scanning releve.png"
  And la sortie stderr contient "INFO scan terminé : 3 fichier(s) traité(s)"
  And le code de retour est 0

Scenario: Scan d'un dossier vide
  Given un dossier vide
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier-vide"
  Then la sortie stdout est le JSON {"scanned": 0, "files": []} avec une liste vide
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

Scenario: Scan retourne les métadonnées de chaque fichier
  Given un dossier contenant 1 fichier : "facture.pdf"
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier"
  Then la sortie stdout contient un objet JSON par fichier avec les champs "name", "uri", "metadata"
  And "metadata" contient "mime_type", "size_bytes", "modified_at"
  And les champs "title", "author", "page_count", "language" sont présents (peuvent être null)
  And le code de retour est 0

Scenario: Extraction échouée sur un fichier — le scan continue
  Given un dossier contenant 2 fichiers dont un corrompu
  When l'utilisateur exécute "archivist scan --source file:///path/to/dossier"
  Then la sortie stdout liste les 2 fichiers
  And le fichier corrompu a "metadata": null
  And la sortie stderr contient "WARNING" pour le fichier corrompu
  And le code de retour est 0
