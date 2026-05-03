Feature: Appliquer les règles de nommage des fichiers du référentiel

  Les règles de nommage garantissent l'homogénéité et la lisibilité de l'arborescence documentaire.
  Elles facilitent le tri chronologique, la recherche et l'interopérabilité entre systèmes
  d'exploitation.

  Scenario Outline: Nommage conforme selon le dossier
    Given un fichier dans le dossier "<dossier>"
    When le fichier est nommé "<nom_fichier>"
    Then le nom est conforme aux règles de nommage

    Examples:
      | dossier                  | nom_fichier                                  |
      | Mes ventes/Factures      | 2026-03_facture_client-dupont_003.pdf         |
      | Mes achats/Factures      | 2026-03_facture_orange_012.pdf                |
      | Mon social               | 2026-03_fiche-paie_dupont-jean.pdf            |
      | Ma fiscalité             | 2026-01_declaration_tva.pdf                   |
      | Ma banque                | 2026-03_releve_banque-populaire.pdf           |

  Scenario: Un fichier avec des accents est non conforme
    Given un fichier nommé "2026-03_facture_société-générale_001.pdf"
    When je vérifie la conformité du nom
    Then le nom est rejeté car il contient des accents

  Scenario: Un fichier avec des espaces est non conforme
    Given un fichier nommé "2026-03 facture dupont 003.pdf"
    When je vérifie la conformité du nom
    Then le nom est rejeté car il contient des espaces

  Scenario: Un fichier avec une date mal formatée est non conforme
    Given un fichier nommé "03-2026_facture_dupont_003.pdf"
    When je vérifie la conformité du nom
    Then le nom est rejeté car la date n'est pas au format "AAAA-MM"

  Scenario: Un fichier en majuscules est non conforme
    Given un fichier nommé "2026-03_FACTURE_Dupont_003.pdf"
    When je vérifie la conformité du nom
    Then le nom est rejeté car il contient des majuscules

  Scenario: Les tirets séparent les mots dans un segment, les underscores séparent les segments
    Given un fichier nommé "2026-03_facture_client-dupont_003.pdf"
    When j'analyse la structure du nom
    Then les segments sont "2026-03", "facture", "client-dupont" et "003"
    And le séparateur entre segments est le underscore
    And le séparateur dans un segment est le tiret
