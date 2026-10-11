Feature: Configuration persistante de la CLI notes

  Pour ne pas répéter ses choix à chaque invocation, l'utilisateur persiste
  l'agent via "notes config set agent" et le dossier du bloc-notes via
  "notes config set bloc-notes".
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

  Scenario: Enregistrer l'agent dans la config
    When l'utilisateur lance "notes config set agent claude-code"
    Then la sortie est {"agent": "claude-code"}
    And la config persistée contient agent = "claude-code"
    And le code de sortie est 0

  Scenario: Enregistrer le dossier bloc-notes
    Given le dossier "/home/alice/bloc" existe
    When l'utilisateur lance "notes config set bloc-notes /home/alice/bloc"
    Then la sortie est {"bloc-notes": "/home/alice/bloc"}
    And la config persistée contient bloc-notes = "/home/alice/bloc"
    And le code de sortie est 0

  Scenario: Un chemin bloc-notes relatif est enregistré en absolu
    Given le dossier courant contient le sous-dossier "bloc"
    When l'utilisateur lance "notes config set bloc-notes bloc"
    Then la config persistée contient le chemin absolu du dossier "bloc"
    And le code de sortie est 0

  Scenario: Un chemin bloc-notes inexistant est refusé
    When l'utilisateur lance "notes config set bloc-notes /chemin/inexistant"
    Then un message d'erreur est affiché
    And la config persistée n'est pas modifiée
    And le code de sortie est 2

  Scenario: Afficher la configuration persistée
    Given l'utilisateur a lancé "notes config set agent claude-code"
    When l'utilisateur lance "notes config show"
    Then la sortie est {"agent": "claude-code"}
    And le code de sortie est 0

  Scenario: Config show ignore les clés inconnues
    Given la config persistée contient agent = "claude-code" et une clé inconnue
    When l'utilisateur lance "notes config show"
    Then la sortie JSON contient uniquement la clé agent
    And le code de sortie est 0

  Scenario: Une ancienne clé llm est ignorée
    Given la config persistée contient llm = "claude-cli"
    When l'utilisateur lance "notes config show"
    Then la sortie est l'objet JSON vide {}
    And le code de sortie est 0

  Scenario: Un nom d'agent inconnu est refusé
    Given la config persistée contient agent = "claude-code"
    When l'utilisateur lance "notes config set agent inconnu"
    Then un message d'erreur liste les valeurs possibles dont "claude-code"
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
    Given le fichier de config contient agent: 2024-01-01
    When l'utilisateur lance "notes config show"
    Then un message d'erreur est affiché sur stderr
    And le code de sortie est 1
