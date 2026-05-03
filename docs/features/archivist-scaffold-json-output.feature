Feature: Émettre une sortie JSON structurée depuis scaffold

  La commande "archivist scaffold" émet un objet JSON sur stdout à la fin de son exécution.
  Ce format permet à un agent ou un script d'analyser le résultat sans parser de texte libre,
  et d'itérer en cas d'erreur.

  Scenario: Succès — le JSON contient les chemins créés
    Given un scaffold exécuté avec succès
    When je lis la sortie JSON sur stdout
    Then le JSON contient les champs "created", "skipped" et "errors" avec des valeurs entières
    And le JSON contient le champ "created_paths" avec la liste des chemins relatifs créés
    And le champ "error_details" est une liste vide

  Scenario: Erreur partielle — le JSON contient les détails d'erreur
    Given un scaffold avec au moins un conflit de chemin
    When je lis la sortie JSON sur stdout
    Then le champ "errors" est supérieur à zéro
    And le champ "error_details" contient une description pour chaque erreur
    And aucune stacktrace Python n'apparaît dans la sortie

  Scenario: Erreur fatale — pas de JSON, message sur stderr
    Given le fichier referentiel.yaml est introuvable
    When je lance "archivist scaffold"
    Then aucun JSON n'est émis sur stdout
    And un message d'erreur lisible est affiché sur stderr
    And le code de sortie est 1
