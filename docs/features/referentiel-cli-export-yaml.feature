Feature: Exporter les frontmatters du référentiel en YAML

  La commande "export-frontmatters" collecte les frontmatters YAML de tous les fichiers Markdown
  du classement et les agrège dans un fichier YAML unique. Ce fichier sert de source de vérité
  pour les outils en aval (CLI utilisateur, génération PDF).

  Background:
    Given le répertoire "packages/referentiel/classement/" contient des fichiers ".md" avec frontmatter YAML

  Scenario: Export nominal vers le fichier par défaut
    When je lance "referentiel-cli export-frontmatters"
    Then le fichier "packages/referentiel/referentiel.yaml" est généré
    And il contient une liste d'entrées triées par "id" en ordre lexicographique
    And chaque entrée contient les champs "id", "folder_name", "path", "option" et "required"

  Scenario: Export vers un chemin personnalisé
    When je lance "referentiel-cli export-frontmatters --output /tmp/export.yaml"
    Then le fichier "/tmp/export.yaml" est généré
    And son contenu est identique à celui de l'export par défaut

  Scenario: Un fichier Markdown sans frontmatter provoque une erreur
    Given un fichier "classement/test_sans_frontmatter.md" sans bloc frontmatter
    When je lance "referentiel-cli export-frontmatters"
    Then une erreur signale le fichier sans frontmatter
    And l'export est interrompu

  Scenario: Le fichier "__index.md" est exclu de l'export
    Given le fichier "classement/__index.md" existe
    When je lance "referentiel-cli export-frontmatters"
    Then aucune entrée correspondant à "__index.md" n'apparaît dans le YAML de sortie
