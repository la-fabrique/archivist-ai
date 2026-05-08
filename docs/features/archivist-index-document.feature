Feature: Indexation des documents lors du scan

Pour permettre une future recherche plein-texte dans les documents archivés,
le pipeline de scan indexe le contenu textuel et les métadonnées de chaque document
traité avec succès dans un index persistant.

Background:
  Given le pipeline de scan est configuré avec un index actif

Scenario: Indexation d'un document après extraction réussie
  Given un document "facture.pdf" est présent dans le répertoire de réception
  When le pipeline de scan traite ce document
  Then le document est indexé avec son contenu textuel et ses métadonnées
  And l'index contient une entrée identifiée par l'URI du document

Scenario: Réindexation d'un document déjà présent dans l'index
  Given un document "contrat.pdf" a déjà été indexé lors d'un scan précédent
  When le pipeline de scan traite à nouveau ce document
  Then l'entrée existante dans l'index est remplacée par les nouvelles données
  And l'index ne contient qu'une seule entrée pour ce document

Scenario: Indexation d'un document au contenu vide
  Given un document est présent dans le répertoire de réception
  And l'extraction de ce document produit un contenu textuel vide
  When le pipeline de scan traite ce document
  Then le document est indexé sans erreur
  And l'index contient une entrée pour ce document avec un contenu vide

Scenario: Echec d'indexation sans interruption du scan
  Given plusieurs documents sont présents dans le répertoire de réception
  And l'index rencontre une erreur lors de l'indexation du premier document
  When le pipeline de scan traite ces documents
  Then le scan se poursuit pour les documents suivants
  And les documents sont sauvegardés et supprimés du répertoire de réception
  And l'erreur d'indexation est signalée dans les logs

Scenario: Scan sans index configuré
  Given le pipeline de scan est configuré sans index
  When le pipeline de scan traite des documents
  Then le scan se déroule normalement sans indexation
  And les documents sont sauvegardés et supprimés du répertoire de réception
