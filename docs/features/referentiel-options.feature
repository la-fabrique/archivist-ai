Feature: Filtrer les dossiers du référentiel par options cumulables

  Le référentiel utilise un système d'options cumulables plutôt que des profils prédéfinis.
  L'option "core" est toujours incluse. Les options supplémentaires ajoutent des dossiers
  spécifiques au contexte de l'utilisateur, sans modifier le noyau commun.

  Scenario: L'option "core" inclut les dossiers de base
    Given le référentiel avec les options "core", "dirigeant-assimile-salarie" et "assurances"
    When je sélectionne uniquement l'option "core"
    Then les dossiers "Mes ventes", "Mes achats", "Mon juridique", "Ma fiscalité", "Ma banque" et "Archives" sont inclus
    And les dossiers "Mon social" et "Mes assurances" sont exclus

  Scenario: Ajout de l'option "dirigeant-assimile-salarie"
    Given le référentiel avec les options "core" et "dirigeant-assimile-salarie"
    When je sélectionne les options "core" et "dirigeant-assimile-salarie"
    Then le dossier "Mon social" est inclus en plus des dossiers "core"

  Scenario: Cumul de plusieurs options
    When je sélectionne les options "core", "dirigeant-assimile-salarie" et "assurances"
    Then tous les dossiers du référentiel sont inclus

  Scenario: L'option "core" est toujours implicite
    When je sélectionne uniquement l'option "assurances"
    Then les dossiers "core" sont inclus automatiquement
    And le dossier "Mes assurances" est également inclus
