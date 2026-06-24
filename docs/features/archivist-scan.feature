Feature: Scanner le dossier de réception

Pour permettre au pipeline de traitement de documents d'ingérer les fichiers déposés,
la commande scan lit les fichiers du dossier _Réception défini dans le référentiel,
sauvegarde chaque original dans _Conservation brut (archive zip horodatée) et extrait les
métadonnées. Les fichiers restent dans _Réception après scan — leur déplacement définitif
est effectué par la commande apply après classification. Sans backup réussi, aucun fichier
n'est traité.

Background:
  Given l'outil archivist est installé
  And un référentiel contenant une entrée "role: reception" pointant vers "_Réception"
  And un référentiel contenant une entrée "role: conservation_brut" pointant vers "_Conservation brut"

Scenario: Scan nominal — backup et extraction sans suppression
  Given un dossier "_Réception" contenant 3 fichiers : "facture.pdf", "contrat.pdf", "releve.png"
  And un dossier "_Conservation brut" vide
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then la sortie stdout est un JSON avec "scanned": 3, "backed_up": 3
  And "files" contient 3 objets avec les champs "name", "uri", "metadata"
  And le dossier "_Conservation brut" contient 3 archives zip nommées "<nom>_<timestamp>.zip"
  And le dossier "_Réception" contient toujours les 3 fichiers originaux
  And la sortie stderr contient "INFO scanning facture.pdf"
  And le code de retour est 0

Scenario: Scan d'un dossier _Réception vide
  Given un dossier "_Réception" vide
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then la sortie stdout est le JSON {"scanned": 0, "backed_up": 0, "files": []}
  And le code de retour est 0

Scenario: Le scan est non récursif
  Given un dossier "_Réception" contenant 2 fichiers et 1 sous-dossier avec 3 fichiers supplémentaires
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then la sortie stdout liste uniquement les 2 fichiers du niveau racine
  And les fichiers du sous-dossier ne sont pas inclus dans "files"
  And "scanned": 2

Scenario: Échec du backup — le fichier n'est ni extrait ni supprimé
  Given un dossier "_Réception" contenant 1 fichier "facture.pdf"
  And le système de fichiers ne peut pas créer de zip dans "_Conservation brut"
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then la sortie stdout est le JSON {"scanned": 0, "backed_up": 0, "files": []}
  And le fichier "facture.pdf" est toujours présent dans "_Réception"
  And la sortie stderr contient "ERROR" mentionnant le fichier concerné
  And le code de retour est 0

Scenario: Extraction échouée sur un fichier — le scan continue, le fichier reste dans _Réception
  Given un dossier "_Réception" contenant 2 fichiers dont un corrompu
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then la sortie stdout liste les 2 fichiers avec "backed_up": 2
  And le fichier corrompu a "metadata": null
  And la sortie stderr contient "WARNING" pour le fichier corrompu
  And les 2 fichiers sont toujours présents dans "_Réception"
  And le code de retour est 0

Scenario: Scan retourne les métadonnées de chaque fichier
  Given un dossier "_Réception" contenant 1 fichier "facture.pdf"
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then "metadata" contient "mime_type", "size_bytes", "modified_at"
  And les champs "title", "author", "page_count", "language" sont présents (peuvent être null)
  And le code de retour est 0

Scenario: Option --referentiel manquante
  When l'utilisateur exécute "archivist scan --root file:///path/to/archive"
  Then le code de retour est 2
  And la sortie stderr contient un message d'erreur mentionnant "--referentiel"

Scenario: URI --referentiel avec schéma invalide
  When l'utilisateur exécute "archivist scan --referentiel /chemin/sans/scheme --root file:///path/to/archive"
  Then le code de retour est 2

Scenario: Dossier _Réception absent de l'archive cible
  Given un dossier cible sans dossier "_Réception"
  When l'utilisateur exécute "archivist scan --referentiel file:///path/to/referentiel.yaml --root file:///path/to/archive"
  Then le code de retour est 2
  And la sortie stderr contient "scaffold" dans le message d'erreur
