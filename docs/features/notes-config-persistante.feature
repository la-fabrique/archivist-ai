Feature: Configuration persistante de la CLI notes

  Pour ne pas répéter le choix de l'adaptateur LLM à chaque invocation,
  l'utilisateur le persiste via "notes config set llm".
  La configuration est stockée dans le dossier app data de l'utilisateur
  (platformdirs, application "notes") au format YAML et relue par "notes config show".

  Scenario: Lancer notes sans argument affiche l'aide
    When l'utilisateur lance "notes" sans argument
    Then l'aide de la CLI est affichée
    And le code de sortie est 0

  Scenario: Afficher la configuration quand rien n'est persisté
    Given aucune configuration n'a été enregistrée
    When l'utilisateur lance "notes config show"
    Then la sortie est l'objet JSON vide {}
    And le code de sortie est 0

  Scenario: Enregistrer l'adaptateur LLM dans la config
    When l'utilisateur lance "notes config set llm claude-cli"
    Then la sortie est {"llm": "claude-cli"}
    And la config persistée contient llm = "claude-cli"
    And le code de sortie est 0

  Scenario: Afficher la configuration persistée
    Given l'utilisateur a lancé "notes config set llm claude-cli"
    When l'utilisateur lance "notes config show"
    Then la sortie est {"llm": "claude-cli"}
    And le code de sortie est 0

  Scenario: Config show ignore les clés inconnues
    Given la config persistée contient llm = "claude-cli" et une clé inconnue
    When l'utilisateur lance "notes config show"
    Then la sortie JSON contient uniquement la clé llm
    And le code de sortie est 0

  Scenario: Un nom d'adaptateur LLM inconnu est refusé
    Given la config persistée contient llm = "claude-cli"
    When l'utilisateur lance "notes config set llm inconnu"
    Then un message d'erreur liste les valeurs possibles dont "claude-cli"
    And la config persistée n'est pas modifiée
    And le code de sortie est 2

  Scenario: Un paramètre de configuration inconnu est refusé
    When l'utilisateur lance "notes config set vault file:///notes"
    Then un message d'erreur est affiché
    And le code de sortie est non nul

  Scenario: Une config corrompue produit une erreur claire
    Given le fichier de config contient un YAML invalide
    When l'utilisateur lance "notes config show"
    Then un message d'erreur est affiché sur stderr
    And aucune trace d'exécution n'est affichée
    And le code de sortie est 1

  Scenario: Une valeur non textuelle dans la config produit une erreur claire
    Given le fichier de config contient llm: 2024-01-01
    When l'utilisateur lance "notes config show"
    Then un message d'erreur est affiché sur stderr
    And le code de sortie est 1
