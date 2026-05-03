Feature: Prévisualiser le scaffold sans créer de dossiers

  Le flag "--dry-run" permet à l'utilisateur de vérifier quels dossiers seraient créés
  avant d'exécuter réellement la commande. Aucune modification n'est apportée au disque.

  Background:
    Given un fichier referentiel.yaml valide
    And un répertoire cible vide

  Scenario: Le dry-run affiche les dossiers prévus
    When je lance "archivist scaffold --dry-run"
    Then la sortie stderr liste les dossiers qui seraient créés
    And la sortie JSON sur stdout indique le nombre de dossiers dans le champ "created"

  Scenario: Le dry-run ne crée aucun dossier sur le disque
    When je lance "archivist scaffold --dry-run"
    Then le répertoire cible reste vide
