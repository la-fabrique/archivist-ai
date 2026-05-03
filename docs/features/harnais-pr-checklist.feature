Feature: Valider la qualité avant un commit ou une pull request

  La skill "pr-checklist" exécute une série de vérifications avant qu'un commit ou une PR
  ne soit soumis : tests unitaires, intégrité YAML et propreté des imports. Elle agit comme
  un filet de sécurité pour éviter les régressions.

  Scenario: Toutes les vérifications passent
    Given le code est prêt à être commité
    When la skill pr-checklist est invoquée
    Then les tests unitaires passent
    And le YAML du référentiel est valide
    And les imports sont propres
    And la skill indique que le commit peut procéder

  Scenario: Les tests unitaires échouent
    Given un test unitaire est en échec
    When la skill pr-checklist est invoquée
    Then l'échec des tests est signalé
    And la skill recommande de corriger avant de commiter

  Scenario: Le YAML du référentiel est invalide
    Given le fichier referentiel.yaml contient une erreur de syntaxe
    When la skill pr-checklist est invoquée
    Then l'erreur YAML est signalée avec le détail
    And la skill recommande de corriger avant de commiter

  Scenario: Les vérifications sont indépendantes
    Given un test unitaire est en échec
    And le YAML du référentiel est valide
    When la skill pr-checklist est invoquée
    Then l'échec des tests est signalé
    And la validité du YAML est confirmée
    And toutes les vérifications sont exécutées même si l'une échoue
