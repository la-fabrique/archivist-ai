Feature: Ajouter une idée au bloc-notes

  Pour déposer une idée sans quitter son outil, l'utilisateur (ou un agent appelant)
  la confie au bloc-notes via "notes add idea". Le bloc-notes challenge l'idée et la range ;
  la CLI ne fait que le pont : elle transmet le message à l'agent configuré, qui travaille
  dans le dossier du bloc-notes, puis affiche la réponse en JSON sans l'interpréter.
  Une conversation peut durer plusieurs tours grâce à l'identifiant de session.

  Background:
    Given l'agent "claude-code" est configuré
    And le dossier du bloc-notes configuré existe

  Scenario: Premier tour avec une idée
    When l'utilisateur lance "notes add idea" avec le texte "Suivre les podcasts de Kristine"
    Then l'agent est lancé dans le dossier du bloc-notes avec la commande "/add Suivre les podcasts de Kristine"
    And un nouvel identifiant de session est généré avant l'appel
    And la sortie est un objet JSON contenant "session", "reponse" et "suite"
    And "reponse" contient le texte brut renvoyé par le bloc-notes
    And "suite" indique la commande pour répondre avec "--session" et "--reply"
    And le code de sortie est 0

  Scenario: Une réponse commençant par un tiret n'est pas prise pour une option
    When l'utilisateur répond avec "--reply" par un texte commençant par "-"
    Then le texte est transmis tel quel à l'agent comme message
    And il n'est pas interprété comme une option de l'agent

  Scenario: Tour suivant pour répondre à une question du bloc-notes
    Given une session "abc123" a été ouverte par un premier tour
    When l'utilisateur lance "notes add idea --session abc123 --reply" avec le texte "Pour ma veille"
    Then la conversation de la session "abc123" est reprise dans le dossier du bloc-notes
    And le texte "Pour ma veille" est transmis comme message
    And la sortie est un objet JSON dont "session" vaut "abc123"
    And "suite" est toujours présent
    And le code de sortie est 0

  Scenario: La CLI ne juge pas du résultat
    Given le bloc-notes répond par une question ou par une confirmation de dépôt
    When la réponse est affichée
    Then la structure de la sortie est identique dans les deux cas
    And c'est à l'appelant de juger à la lecture de "reponse"

  Scenario Outline: Combinaison d'arguments invalide
    When l'utilisateur lance "notes add idea" avec <arguments>
    Then un message d'usage est écrit sur stderr
    And le code de sortie est 2

    Examples:
      | arguments                    |
      | aucun argument               |
      | un texte d'idée et "--reply" |
      | "--reply" sans "--session"   |
      | "--session" sans "--reply"   |
      | un texte d'idée vide         |
      | une réponse vide             |

  Scenario: Agent non configuré
    Given aucun agent n'est configuré
    When l'utilisateur lance "notes add idea" avec le texte "Une idée"
    Then un message indique de lancer "notes config set agent claude-code"
    And le code de sortie est 1

  Scenario: Bloc-notes non configuré
    Given aucun dossier de bloc-notes n'est configuré
    When l'utilisateur lance "notes add idea" avec le texte "Une idée"
    Then un message indique de lancer "notes config set bloc-notes <chemin>"
    And le code de sortie est 1

  Scenario: Dossier du bloc-notes disparu
    Given le dossier du bloc-notes configuré n'existe plus
    When l'utilisateur lance "notes add idea" avec le texte "Une idée"
    Then un message indique que le dossier n'existe plus
    And le code de sortie est 1

  Scenario: Échec pendant l'appel à l'agent après son démarrage
    Given l'agent a démarré mais échoue (délai de 600 s dépassé, code retour non nul, JSON illisible ou erreur signalée)
    When l'utilisateur lance "notes add idea" avec le texte "Une idée"
    Then l'erreur est écrite sur stderr sans trace d'exécution
    And le message donne l'identifiant de session
    And le message donne la commande "notes add idea --session <id> --reply" pour reprendre la conversation
    And le code de sortie est 1

  Scenario: Agent introuvable
    Given la commande de l'agent est absente ou non exécutable
    When l'utilisateur lance "notes add idea" avec le texte "Une idée"
    Then l'erreur est écrite sur stderr
    And aucun rappel de reprise de session n'est affiché car aucune session n'existe
    And le code de sortie est 1
