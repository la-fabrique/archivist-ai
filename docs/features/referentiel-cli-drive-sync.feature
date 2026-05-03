Feature: Synchroniser le référentiel vers Google Drive

  La commande "push-drive" permet de pousser le contenu du référentiel vers un dossier
  Google Drive existant. Elle sert à partager le référentiel avec des utilisateurs qui
  consultent leurs documents depuis Drive.

  Scenario: Synchronisation nominale
    Given l'utilisateur est authentifié auprès de Google Drive
    And un dossier cible Drive existe avec un identifiant connu
    When je lance "referentiel-cli push --parent-folder-id <id>"
    Then les fichiers de "packages/referentiel/" sont synchronisés dans le dossier Drive
    And les dossiers manquants sont créés dans Drive
    And les fichiers modifiés sont mis à jour

  Scenario: Un fichier non modifié est ignoré
    Given un fichier déjà synchronisé dont le contenu n'a pas changé
    When je lance "referentiel-cli push --parent-folder-id <id>"
    Then le fichier n'est pas re-uploadé

  Scenario: Le mode dry-run n'écrit rien sur Drive
    Given l'utilisateur est authentifié auprès de Google Drive
    When je lance "referentiel-cli push --parent-folder-id <id> --dry-run"
    Then la liste des opérations prévues est affichée
    And aucune modification n'est effectuée sur Drive

  Scenario: Authentification manquante
    Given l'utilisateur n'est pas authentifié auprès de Google Drive
    When je lance "referentiel-cli push --parent-folder-id <id>"
    Then un message d'erreur indique que l'authentification est requise
    And la commande retourne un code d'erreur
