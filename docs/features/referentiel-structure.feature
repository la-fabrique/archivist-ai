Feature: Structurer le référentiel en dossiers avec frontmatter YAML

  Le référentiel documentaire est la base de connaissances partagée avec les TPE et indépendants.
  Chaque dossier du plan de classement doit avoir son propre fichier Markdown avec un frontmatter
  YAML structuré, afin de permettre l'export automatisé et la génération d'outils à partir d'une
  source unique.

  Background:
    Given le répertoire "packages/referentiel/classement/" contient les fichiers Markdown du référentiel

  Scenario: Chaque dossier du plan de classement possède un fichier Markdown
    When je liste les fichiers ".md" dans "classement/"
    Then chaque dossier décrit dans le plan de classement a un fichier ".md" correspondant
    And les fichiers sont nommés en snake_case avec le séparateur "__" pour la hiérarchie

  Scenario: Chaque fichier Markdown contient un frontmatter YAML valide
    When je lis un fichier ".md" du classement
    Then il contient un bloc frontmatter YAML entre "---"
    And le frontmatter contient les champs obligatoires "id", "folder_name", "path", "dynamic", "option", "required" et "description"

  Scenario: La hiérarchie parent-enfant est cohérente
    Given un fichier enfant avec le champ "parent" renseigné
    When je vérifie la valeur du champ "parent"
    Then elle correspond à l'identifiant "id" d'un autre fichier du classement

  Scenario: Les dossiers racine n'ont pas de parent
    When je lis un fichier racine comme "mes_ventes.md"
    Then le champ "parent" est absent du frontmatter

  Scenario: Les dossiers purement chronologiques n'ont pas de fichier Markdown
    Given un dossier parent dont l'organisation est de type "chronological" avec le pattern "AAAA-MM"
    Then aucun fichier ".md" n'existe pour les sous-dossiers chronologiques
    And l'organisation chronologique est décrite dans le frontmatter du parent
