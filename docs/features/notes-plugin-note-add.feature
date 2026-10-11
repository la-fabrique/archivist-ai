Feature: Déposer une idée dans le bloc-notes depuis Claude Code avec le plugin notes

  Pour confier une idée au bloc-notes sans quitter sa session Claude Code, l'utilisateur
  installe le plugin "notes" et lance "/notes:note-add". Le plugin installe lui-même la CLI
  "notes" au démarrage de la session. Le skill ne fait que le pont : il transmet l'idée telle
  quelle, montre chaque réponse du bloc-notes mot pour mot et attend l'utilisateur à chaque question.

  Scenario: Installation de la CLI au démarrage de la session
    Given le plugin "notes" est installé depuis la marketplace du dépôt
    And la plateforme est Linux x86_64 ou macOS arm64
    When une session Claude Code démarre
    Then la dernière version publiée de la CLI "notes" est téléchargée dans le dossier de données du plugin
    And la version installée est mémorisée
    And le démarrage de la session n'est jamais bloqué

  Scenario: Version déjà à jour
    Given la dernière version de la CLI est déjà installée
    When une session Claude Code démarre
    Then aucun téléchargement n'a lieu

  Scenario: Échec silencieux de l'installation
    Given la plateforme n'est pas prise en charge ou le réseau est indisponible
    When une session Claude Code démarre
    Then aucune erreur n'est affichée
    And la session démarre normalement

  Scenario: CLI pas encore installée
    Given la CLI n'a pas encore été installée par le plugin
    When la commande "notes" est lancée
    Then un message indique que la CLI n'est pas encore installée
    And le message invite à redémarrer la session ou à l'installer manuellement
    And le code de sortie est 127

  Scenario: CLI installée à la main prioritaire
    Given une CLI "notes" est installée ailleurs sur le PATH de l'utilisateur
    When la commande "notes" est lancée
    Then c'est la CLI de l'utilisateur qui est utilisée, pas celle du plugin

  Scenario: Idée acceptée après une question du bloc-notes
    Given la CLI est installée et configurée
    When l'utilisateur lance "/notes:note-add" avec l'idée "Un export PDF des fiches"
    Then l'idée est transmise telle quelle à "notes add idea"
    And la réponse du bloc-notes est affichée mot pour mot
    And le skill attend la réponse de l'utilisateur sans répondre à sa place
    When l'utilisateur répond "Diffusion à des tiers"
    Then cette réponse est transmise telle quelle avec la session et "--reply"
    And la confirmation de dépôt est affichée
    And aucun autre tour n'est lancé

  Scenario: Idée contenant des caractères spéciaux
    When l'utilisateur lance "/notes:note-add" avec une idée commençant par "-" ou contenant des guillemets, "$" ou des backticks
    Then le texte est transmis sans interprétation par le shell ni comme option

  Scenario: Idée absente
    When l'utilisateur lance "/notes:note-add" sans argument
    Then le skill demande l'idée à l'utilisateur
    And n'appelle la CLI qu'après sa réponse

  Scenario: Doute sur la nature de la réponse
    Given la réponse du bloc-notes n'est ni clairement une question ni une confirmation
    When elle est affichée
    Then elle est traitée comme une question
    And le skill attend l'utilisateur

  Scenario: Abandon pendant l'échange
    Given le bloc-notes a posé une question
    When l'utilisateur demande d'arrêter
    Then la CLI n'est plus appelée
    And la commande pour reprendre la conversation plus tard est affichée

  Scenario: Agent non configuré
    Given aucun agent n'est configuré
    When l'utilisateur lance "/notes:note-add" avec une idée
    Then le skill lance "notes config set agent claude-code" sans demander
    And relance le tour en cours une seule fois

  Scenario: Bloc-notes non configuré ou disparu
    Given aucun dossier de bloc-notes n'est configuré, ou il n'existe plus
    When l'utilisateur lance "/notes:note-add" avec une idée
    Then le skill demande le chemin du bloc-notes à l'utilisateur
    And lance "notes config set bloc-notes" avec ce chemin
    And relance le tour en cours une seule fois

  Scenario: Chemin de bloc-notes refusé
    Given le chemin fourni n'est pas un dossier existant
    When le skill lance "notes config set bloc-notes"
    Then le message est affiché et le chemin est redemandé
    And l'utilisateur peut renoncer, ce qui arrête le skill

  Scenario: Même erreur de configuration après correction
    Given le skill vient de configurer l'agent ou le bloc-notes et de relancer le tour
    When la même erreur de configuration revient
    Then l'erreur est affichée
    And le skill s'arrête

  Scenario: Échec de l'agent en cours d'échange
    Given l'agent a démarré mais échoue
    When le skill reçoit l'erreur avec la commande "--session" de reprise
    Then l'erreur est affichée
    And la reprise est proposée à l'utilisateur
    And rien n'est relancé automatiquement car le bloc-notes a pu écrire avant l'interruption

  Scenario: Autre erreur
    Given la CLI échoue avec un autre message
    When le skill reçoit l'erreur
    Then le message est affiché tel quel
    And le skill s'arrête
