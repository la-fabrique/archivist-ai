# Raccourcis et liens

> Partie du [Référentiel de gestion documentaire](./_index.md) — v0

---

## Principe directeur

Un document ne vit qu'à **un seul endroit physique** — son dossier de classement naturel (par type et par période). Quand tu as besoin de retrouver ce document depuis un autre angle (par client, par projet, par thème), tu crées un **raccourci**, jamais une copie.

**Pourquoi interdire les copies ?**

La duplication crée des incohérences. Laquelle des deux versions est la bonne ? Celle-ci a été corrigée, celle-là non. Avec un raccourci, il n'existe qu'une source de vérité — la modifier, c'est la modifier partout.

---

## Cas d'usage principal : la vue par client

Le problème : les factures d'un client sont dans un dossier chronologique séparé de son dossier client.

- Sa facture est dans `Mes ventes/Mes factures clients/2026-03/`
- Son contrat et ses devis sont dans `Mes ventes/Mes clients/Dupont/`

C'est logique pour le classement global, mais difficile quand tu veux voir **toutes les factures de ce client** depuis son dossier.

La solution : le dossier `Mes ventes/Mes clients/Dupont/` contient des raccourcis vers les factures du client.

```
Mes ventes/Mes clients/
├── Dupont/
│   ├── Contrats/
│   ├── Devis/
│   ├── Offres/
│   ├── → Mes factures clients/2026-03/2026-03_Facture_Dupont_F2600003.pdf
│   └── → Mes factures clients/2026-02/2026-02_Facture_Dupont_F2600002.pdf
└── Martin/
    ├── Contrats/
    ├── Devis/
    ├── Offres/
    └── → Mes factures clients/2026-02/2026-02_Facture_Martin_F2600001.pdf
```

Tu vois l'ensemble du dossier client en un coup d'œil, sans avoir dupliqué un seul fichier.

---

## Implémentation selon ton système

| Système | Mécanisme | Comment faire |
|---------|-----------|--------------|
| **Windows** | Raccourci `.lnk` | Clic droit sur le fichier → "Créer un raccourci", déplacer le raccourci dans `Mes clients/Dupont/` |
| **macOS** | Alias | Option+Cmd+drag du fichier vers le dossier cible, ou clic droit → "Créer un alias" |
| **Linux** | Lien symbolique | `ln -s /chemin/original /chemin/raccourci` |
| **Google Drive** | Raccourci Drive | Clic droit sur le fichier → "Ajouter un raccourci vers Drive" → choisir le dossier |
| **OneDrive / SharePoint** | Fichier `.url` ou `.md` avec lien | Support des raccourcis limité — alternative : créer un fichier `.md` listant les liens vers les documents |

**Note OneDrive / SharePoint :** la gestion des raccourcis dans ces environnements est moins native. Si tu utilises OneDrive, la solution la plus robuste est un fichier `liens.md` dans le dossier client qui liste les chemins vers les documents. Moins élégant, mais fiable.

---

## Règles

**Un raccourci n'est pas un document.** Si l'original est archivé ou déplacé, le raccourci devient mort (il pointe vers rien). C'est normal — c'est le signe qu'il faut le nettoyer.

**Pas de raccourci vers un raccourci.** Toujours pointer vers le fichier original. Sinon, si l'original bouge, la chaîne se casse en plusieurs endroits.

**Même nom que l'original.** Le dossier parent (ex: `Dupont/`) donne le contexte. Le raccourci garde le nom du fichier original pour éviter toute ambiguïté.

**Nettoyage lors de l'archivage annuel.** Quand les documents d'une année passent dans `Archives/`, les raccourcis correspondants dans `Mes clients/` doivent être supprimés. Un raccourci mort dans `Mes clients/Dupont/` ne fait que créer de la confusion.

---

## Quand créer un raccourci

| Situation | À faire |
|-----------|---------|
| Voir les factures d'un client depuis son dossier | Raccourci dans `Mes ventes/Mes clients/{nom_client}/` |
| Accéder rapidement à un document consulté souvent | Raccourci dans un dossier `raccourcis/` personnel à la racine |
| Un document concerne deux clients | Un raccourci dans le dossier de chaque client |
| Vouloir "copier" un document dans deux dossiers | **Toujours un raccourci, jamais une copie** |
| Document d'archive à garder sous la main temporairement | Raccourci temporaire — à supprimer quand ce n'est plus utile |

---

## Limites connues

Les raccourcis ne fonctionnent pas de manière uniforme entre systèmes. Un raccourci `.lnk` Windows ne s'ouvre pas sur macOS. Un alias macOS ne fonctionne pas sur Linux. Si tu travailles en équipe sur des systèmes différents, la gestion des raccourcis demande une convention commune.

C'est une limite réelle du référentiel v0. Quand l'agent IA sera en place, il gérera la création, la mise à jour et le nettoyage des raccourcis automatiquement, en s'adaptant au système de stockage de chaque utilisateur.
