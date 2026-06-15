Feature: Configuration persistante de la CLI archivist

  Pour éviter de passer --referentiel, --root et --llm à chaque invocation,
  l'utilisateur peut persister ces paramètres via "archivist config set".
  Ils sont stockés dans le dossier app data de l'utilisateur (platformdirs)
  et utilisés en fallback par toutes les commandes qui en ont besoin.

  Background:
    Given l'utilisateur dispose d'un fichier referentiel.yaml valide

  Scenario: Enregistrer le référentiel dans la config
    When l'utilisateur lance "archivist config set referentiel file:///chemin/referentiel.yaml"
    Then le fichier est copié dans le dossier app data
    And la config persistée pointe vers la copie dans le dossier app data
    And le code de sortie est 0

  Scenario: Enregistrer le dossier racine dans la config
    When l'utilisateur lance "archivist config set root file:///chemin/archive"
    Then la config persistée contient root = "file:///chemin/archive"
    And le code de sortie est 0

  Scenario: Enregistrer l'adaptateur LLM dans la config
    When l'utilisateur lance "archivist config set llm claude-cli"
    Then la config persistée contient llm = "claude-cli"
    And le code de sortie est 0

  Scenario: Afficher la configuration persistée
    Given la config contient referentiel, root et llm
    When l'utilisateur lance "archivist config show"
    Then la sortie est un objet JSON avec les clés referentiel, root et llm
    And le code de sortie est 0

  Scenario: Config show n'affiche pas les clés absentes
    Given la config ne contient que llm
    When l'utilisateur lance "archivist config show"
    Then la sortie JSON contient uniquement la clé llm
    And les clés referentiel et root sont absentes de la sortie

  Scenario: config set referentiel échoue si le fichier source est absent
    When l'utilisateur lance "archivist config set referentiel file:///inexistant/ref.yaml"
    Then un message d'erreur est affiché
    And le code de sortie est non nul

  Scenario: config set referentiel échoue si l'URI n'est pas file://
    When l'utilisateur lance "archivist config set referentiel /chemin/sans/scheme"
    Then un message d'erreur indique que le schéma file:// est requis
    And le code de sortie est non nul

  Scenario: scaffold sans arguments utilise la config persistée
    Given la config persistée contient referentiel et root
    And le répertoire root est vide
    When l'utilisateur lance "archivist scaffold" sans passer --referentiel ni --root
    Then les dossiers du référentiel sont créés dans le répertoire root
    And le code de sortie est 0

  Scenario: L'argument CLI est prioritaire sur la config persistée
    Given la config persistée contient referentiel et root
    And un autre répertoire cible existe
    When l'utilisateur lance "archivist scaffold --root file:///autre/cible"
    Then les dossiers sont créés dans l'autre répertoire cible
    And le répertoire de la config n'est pas modifié

  Scenario: scaffold échoue avec message clair si referentiel manquant
    Given la config ne contient pas de referentiel
    When l'utilisateur lance "archivist scaffold --root file:///chemin/archive"
    Then un message d'erreur mentionne "referentiel"
    And le message suggère "archivist config set referentiel"
    And le code de sortie est non nul

  Scenario: scaffold échoue avec message clair si root manquant
    Given la config ne contient pas de root
    When l'utilisateur lance "archivist scaffold --referentiel file:///chemin/ref.yaml"
    Then un message d'erreur mentionne "root"
    And le message suggère "archivist config set root"
    And le code de sortie est non nul
