Feature: Déclencher un rappel lors de la modification du référentiel

  Le hook PreToolUse "referentiel-guard" détecte quand un fichier de "packages/referentiel/"
  est modifié via Write ou Edit, et injecte un rappel pour invoquer la skill referentiel-update.
  Cela garantit que les modifications du référentiel suivent le processus de qualification en
  4 étapes.

  Scenario: Modification d'un fichier du référentiel
    Given un appel Write sur un fichier dans "packages/referentiel/"
    When le hook referentiel-guard s'exécute
    Then il autorise l'opération
    And il injecte un rappel contenant "referentiel-update" dans le contexte de l'agent

  Scenario: Modification d'un fichier hors du référentiel
    Given un appel Write sur un fichier dans "packages/archivist-cli/"
    When le hook referentiel-guard s'exécute
    Then il ne produit aucune sortie
    And l'opération se poursuit normalement

  Scenario: Appel d'un outil autre que Write ou Edit
    Given un appel Bash sur un fichier quelconque
    When le hook referentiel-guard s'exécute
    Then il ne produit aucune sortie
