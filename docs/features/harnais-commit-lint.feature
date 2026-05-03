Feature: Valider le format des messages de commit

  Le hook PostToolUse "commit-lint" vérifie que les messages de commit suivent le format
  conventional commits : "type(scope): description". Il émet un avertissement dans le
  contexte de l'agent si le message est non conforme, sans bloquer l'opération.

  Scenario Outline: Message de commit conforme
    Given un appel Bash contenant "git commit -m '<message>'"
    When le hook commit-lint s'exécute
    Then il ne produit aucune sortie

    Examples:
      | message                                      |
      | feat(archivist-cli): add dry-run flag         |
      | fix(referentiel): correct broken link         |
      | docs(harnais): add hooks plan                 |
      | test(archivist-cli): add scaffold unit tests  |
      | chore(ci): update workflow                    |

  Scenario: Message de commit non conforme
    Given un appel Bash contenant "git commit -m 'add some stuff'"
    When le hook commit-lint s'exécute
    Then il émet un avertissement contenant "HARNAIS WARNING"
    And l'avertissement rappelle le format attendu "type(scope): description"

  Scenario: Commande Bash sans git commit
    Given un appel Bash contenant "uv run pytest tests/ -q"
    When le hook commit-lint s'exécute
    Then il ne produit aucune sortie
