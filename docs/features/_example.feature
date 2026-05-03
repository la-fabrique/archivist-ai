Feature: VerificationOverTimeImpl ne doit pas dépendre strictement de JUnit

Pour que Mockito puisse être utilisé dans des environnements sans JUnit (ex. TestNG, applications Java pures), les classes internes ne doivent pas avoir de références directes aux classes JUnit dans leurs signatures ou blocs catch susceptibles d'empêcher le chargement de classe en l'absence de JUnit.

Scenario: Chargement sans JUnit
Given un chargeur de classes qui exclut explicitement les packages "junit"
When je charge "VerificationOverTimeImpl"
Then la classe doit se charger avec succès
And aucune "NoClassDefFoundError" ne doit être levée

Scenario: Nouvelle tentative sur les erreurs d'assertion
Given un mode de vérification encapsulé dans VerificationOverTimeImpl avec un délai d'expiration
And le délégué lève une exception "ArgumentsAreDifferent"
When verify est appelé
Then l'exception doit être interceptée And la vérification doit être relancée jusqu'à expiration du délai