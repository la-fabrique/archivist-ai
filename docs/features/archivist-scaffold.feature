Feature: Créer l'arborescence de dossiers depuis le référentiel

  La commande "archivist scaffold" génère l'arborescence de dossiers comptables sur le disque
  à partir du fichier referentiel.yaml. Elle permet à un utilisateur TPE ou indépendant
  d'initialiser son plan de classement en une seule commande.

  Scenario: Création nominale dans un répertoire vide
    Given un fichier referentiel.yaml valide
    And un répertoire cible vide
    When je lance "archivist scaffold --referentiel file://<chemin>/referentiel.yaml --root file://<cible>"
    Then les dossiers statiques du référentiel sont créés dans le répertoire cible
    And la sortie JSON sur stdout indique le nombre de dossiers créés

  Scenario: Les dossiers dynamiques ne sont pas créés
    Given le référentiel contient des entrées avec des placeholders entre crochets dans le chemin
    When je lance "archivist scaffold"
    Then aucun dossier contenant "[" dans son nom n'est créé sur le disque

  Scenario: Réexécution idempotente sur des dossiers existants
    Given l'arborescence a déjà été créée par un précédent scaffold
    When je relance "archivist scaffold" avec les mêmes paramètres
    Then aucun dossier n'est recréé
    And la sortie JSON indique les dossiers ignorés dans le champ "skipped"

  Scenario: Conflit avec un fichier existant au même chemin
    Given un fichier ordinaire existe à l'emplacement d'un dossier attendu
    When je lance "archivist scaffold"
    Then une erreur est comptabilisée pour ce chemin
    And les autres dossiers sont créés normalement
    And le code de sortie est 1

  Scenario: Référentiel YAML absent
    Given le chemin du référentiel pointe vers un fichier inexistant
    When je lance "archivist scaffold"
    Then un message d'erreur est affiché sur stderr
    And aucun JSON n'est émis sur stdout
    And le code de sortie est 1
