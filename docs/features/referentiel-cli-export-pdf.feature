Feature: Générer un PDF lisible du référentiel

  La commande "generate-pdf" produit un document PDF stylé à destination des utilisateurs
  non-techniques (TPE, indépendants). Le PDF offre une vue complète et imprimable du
  référentiel documentaire.

  Background:
    Given le répertoire "packages/referentiel/" contient les fichiers sources du référentiel

  Scenario: Génération nominale du PDF
    When je lance "referentiel-cli generate-pdf"
    Then un fichier PDF est généré dans le répertoire de sortie par défaut
    And le PDF est lisible et non vide

  Scenario: Le PDF contient une page de couverture
    When je génère le PDF du référentiel
    Then la première page contient le titre du référentiel
    And la première page contient la date de génération

  Scenario: Le PDF contient un tableau récapitulatif des dossiers
    When je génère le PDF du référentiel
    Then le PDF contient un tableau listant les dossiers racine
    And chaque ligne du tableau indique le nom du dossier et son rôle

  Scenario: Les options sont prises en compte dans le PDF
    When je génère le PDF avec les options "core" et "assurances"
    Then le PDF inclut les dossiers "core" et "assurances"
    And les dossiers "dirigeant-assimile-salarie" sont absents du PDF
