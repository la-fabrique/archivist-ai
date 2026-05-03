Feature: Filtrer les dossiers créés par scaffold via les options

  La commande "archivist scaffold" ne crée par défaut que les dossiers de l'option "core".
  L'utilisateur peut ajouter des options supplémentaires pour inclure des dossiers spécifiques
  à sa situation (dirigeant assimilé salarié, assurances).

  Background:
    Given un fichier referentiel.yaml valide contenant des entrées "core", "dirigeant-assimile-salarie" et "assurances"
    And un répertoire cible vide

  Scenario: Par défaut seul "core" est inclus
    When je lance "archivist scaffold" sans option supplémentaire
    Then seuls les dossiers marqués "core" sont créés
    And les dossiers "dirigeant-assimile-salarie" et "assurances" ne sont pas créés

  Scenario: Ajout d'une option supplémentaire
    When je lance "archivist scaffold --option dirigeant-assimile-salarie"
    Then les dossiers "core" et "dirigeant-assimile-salarie" sont créés
    And les dossiers "assurances" ne sont pas créés

  Scenario: Cumul de plusieurs options
    When je lance "archivist scaffold --option dirigeant-assimile-salarie --option assurances"
    Then les dossiers "core", "dirigeant-assimile-salarie" et "assurances" sont tous créés
