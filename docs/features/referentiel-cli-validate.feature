Feature: Valider l'intégrité du référentiel

  Les scripts de validation vérifient mécaniquement que le référentiel est cohérent :
  YAML bien formé, liens Markdown valides, couverture des packages dans CLAUDE.md,
  et unicité des rôles système (reception, conservation_brut).
  Ces vérifications tournent en CI pour détecter les régressions au plus tôt.

  Scenario: Le YAML du référentiel est valide et conforme au schéma
    Given le fichier "packages/referentiel/referentiel.yaml" existe
    When je lance la validation YAML
    Then le fichier est parsé sans erreur
    And chaque entrée contient les champs obligatoires "id", "folder_name", "path", "dynamic", "option" et "required"

  Scenario: Un YAML malformé provoque une erreur
    Given un fichier "referentiel.yaml" contenant du YAML invalide
    When je lance la validation YAML
    Then une erreur de parsing est signalée avec le numéro de ligne

  Scenario: Tous les liens Markdown internes sont valides
    Given les fichiers Markdown du référentiel contiennent des liens internes
    When je lance la validation des liens
    Then tous les liens pointent vers des fichiers existants

  Scenario: Un lien Markdown cassé provoque une erreur
    Given un fichier Markdown contenant un lien vers un fichier inexistant
    When je lance la validation des liens
    Then le lien cassé est signalé avec le fichier source et la cible manquante

  Scenario: Chaque package est documenté dans CLAUDE.md
    Given le fichier "CLAUDE.md" à la racine du dépôt
    When je lance la vérification de couverture
    Then chaque répertoire sous "packages/" est mentionné dans la carte du dépôt de CLAUDE.md

  Scenario: Le référentiel contient exactement un dossier de réception et un dossier de conservation
    Given le fichier "packages/referentiel/referentiel.yaml" contient une entrée "role: reception" et une entrée "role: conservation_brut"
    When je lance "referentiel-cli validate"
    Then la commande affiche "✓ role=reception" et "✓ role=conservation_brut"
    And le code de retour est 0

  Scenario: Absence du rôle reception — erreur de validation
    Given le fichier "packages/referentiel/referentiel.yaml" ne contient aucune entrée avec "role: reception"
    When je lance "referentiel-cli validate"
    Then la commande affiche une erreur mentionnant "role=\"reception\": 0 entrée(s) trouvée(s)"
    And le code de retour est 1

  Scenario: Doublon du rôle conservation_brut — erreur de validation
    Given le fichier "packages/referentiel/referentiel.yaml" contient 2 entrées avec "role: conservation_brut"
    When je lance "referentiel-cli validate"
    Then la commande affiche une erreur mentionnant "role=\"conservation_brut\": 2 entrée(s) trouvée(s)"
    And le code de retour est 1
