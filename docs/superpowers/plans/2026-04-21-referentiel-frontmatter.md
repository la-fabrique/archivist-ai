# Référentiel Front Matter — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Éclater `packages/referentiel/classement/` en un fichier `.md` par dossier (front matter + contenu narratif), puis ajouter la commande CLI `export-frontmatters` qui collecte tous les front matters dans `referentiel.yaml`.

**Architecture:** Chaque `.md` est plat dans `classement/`, nommé avec `__` comme séparateur hiérarchique. Le script TS lit tous les fichiers via `readdirSync`, parse le front matter YAML avec `gray-matter`, trie par `id`, et sérialise en YAML compact. La commande s'enregistre dans le CLI `commander` existant.

**Tech Stack:** TypeScript + Node.js (ESM), Vitest, `gray-matter`, `js-yaml`, `commander` (existant).

---

## Fichiers créés / modifiés

### Script
- Create: `packages/referentiel-cli/src/commands/export-frontmatters.ts`
- Modify: `packages/referentiel-cli/src/cli.ts`
- Modify: `packages/referentiel-cli/package.json` (add `gray-matter`, `js-yaml`, `@types/js-yaml`)
- Create: `packages/referentiel-cli/test/export-frontmatters.test.ts`
- Create: `packages/referentiel/referentiel.yaml` (généré)

### Fichiers classement — réécrits
- `packages/referentiel/classement/mes_ventes.md`
- `packages/referentiel/classement/mes_achats.md`
- `packages/referentiel/classement/mon_social.md`
- `packages/referentiel/classement/ma_fiscalite.md`
- `packages/referentiel/classement/ma_banque.md`
- `packages/referentiel/classement/mes_assurances.md`
- `packages/referentiel/classement/mon_juridique.md`
- `packages/referentiel/classement/archives.md`

### Fichiers classement — créés (sous-dossiers)
**Mes ventes:** `mes_ventes__factures_clients.md`, `mes_ventes__modeles.md`, `mes_ventes__modeles__contrats.md`, `mes_ventes__modeles__devis_offres.md`, `mes_ventes__clients.md`, `mes_ventes__clients__nom_client.md`, `mes_ventes__clients__nom_client__contrats.md`, `mes_ventes__clients__nom_client__devis.md`

**Mes achats:** `mes_achats__factures_fournisseurs.md`, `mes_achats__fournisseurs.md`, `mes_achats__fournisseurs__nom_fournisseur.md`

**Mon social:** `mon_social__fiches_de_paie.md`, `mon_social__dpae.md`, `mon_social__modeles_contrat_travail.md`, `mon_social__salaries.md`, `mon_social__salaries__nom_salarie.md`, `mon_social__salaries__nom_salarie__contrats.md`, `mon_social__declarations_sociales.md`, `mon_social__attestations_urssaf.md`

**Ma fiscalité:** `ma_fiscalite__declarations_tva.md`, `ma_fiscalite__liasses_fiscales.md`, `ma_fiscalite__avis_imposition.md`, `ma_fiscalite__avis_cfe.md`

**Ma banque:** `ma_banque__releves_bancaires.md`, `ma_banque__releves_bancaires__nom_banque.md`, `ma_banque__rib.md`

**Mes assurances:** `mes_assurances__rc_pro.md`, `mes_assurances__mutuelle_prevoyance.md`, `mes_assurances__assurance_locaux.md`

**Mon juridique:** `mon_juridique__statuts.md`, `mon_juridique__kbis.md`, `mon_juridique__pv_decisions.md`, `mon_juridique__registres.md`, `mon_juridique__registres__mouvements_titres.md`, `mon_juridique__registres__decisions.md`, `mon_juridique__baux_domiciliation.md`, `mon_juridique__cgv_mentions_legales.md`, `mon_juridique__marques_licences.md`

**Archives:** `archives__annee.md`

---

## Task 1 : Tests pour export-frontmatters (TDD — écrire les tests d'abord)

**Files:**
- Create: `packages/referentiel-cli/test/export-frontmatters.test.ts`

- [ ] **Step 1.1 : Créer le fichier de test**

`packages/referentiel-cli/test/export-frontmatters.test.ts` :
```typescript
import { mkdirSync, writeFileSync, rmSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { load } from "js-yaml";
import { runExportFrontmatters } from "../src/commands/export-frontmatters.js";

describe("runExportFrontmatters", () => {
  let tmpDir: string;
  let classementDir: string;
  let outputPath: string;

  beforeEach(() => {
    tmpDir = join(tmpdir(), `test-export-${Date.now()}`);
    classementDir = join(tmpDir, "classement");
    outputPath = join(tmpDir, "referentiel.yaml");
    mkdirSync(classementDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("collecte les front matters et ignore __index.md", async () => {
    writeFileSync(join(classementDir, "__index.md"), "# Index\npas de front matter");
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "Relation commerciale sortante"\n---\n# Mes ventes\n`
    );
    writeFileSync(
      join(classementDir, "mes_achats.md"),
      `---\nid: mes_achats\nfolder_name: "Mes achats"\npath: "Mes achats"\noption: core\nrequired: true\ndescription: "Relation commerciale entrante"\n---\n# Mes achats\n`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const yaml = readFileSync(outputPath, "utf-8");
    const entries = load(yaml) as Record<string, unknown>[];
    expect(entries).toHaveLength(2);
    expect(entries.map((e) => e["id"])).not.toContain(undefined);
  });

  it("trie les entrées par id", async () => {
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "test"\n---`
    );
    writeFileSync(
      join(classementDir, "mes_ventes__clients.md"),
      `---\nid: mes_ventes.clients\nfolder_name: "Mes clients"\npath: "Mes ventes/Mes clients"\nparent: mes_ventes\noption: core\nrequired: true\ndescription: "test"\n---`
    );
    writeFileSync(
      join(classementDir, "mes_achats.md"),
      `---\nid: mes_achats\nfolder_name: "Mes achats"\npath: "Mes achats"\noption: core\nrequired: true\ndescription: "test"\n---`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const entries = load(readFileSync(outputPath, "utf-8")) as Record<string, unknown>[];
    expect(entries[0]["id"]).toBe("mes_achats");
    expect(entries[1]["id"]).toBe("mes_ventes");
    expect(entries[2]["id"]).toBe("mes_ventes.clients");
  });

  it("ignore les fichiers .md sans front matter (id absent)", async () => {
    writeFileSync(join(classementDir, "README.md"), "# Readme\npas de front matter\n");
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "test"\n---`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const entries = load(readFileSync(outputPath, "utf-8")) as Record<string, unknown>[];
    expect(entries).toHaveLength(1);
    expect(entries[0]["id"]).toBe("mes_ventes");
  });

  it("écrit un fichier YAML valide", async () => {
    writeFileSync(
      join(classementDir, "mes_ventes.md"),
      `---\nid: mes_ventes\nfolder_name: "Mes ventes"\npath: "Mes ventes"\noption: core\nrequired: true\ndescription: "test"\norganization:\n  type: subdirs\n  fixed_subdirs:\n    - mes_ventes.clients\n---`
    );

    await runExportFrontmatters({ referentielRoot: tmpDir, output: outputPath });

    const entries = load(readFileSync(outputPath, "utf-8")) as Record<string, unknown>[];
    expect(entries[0]).toMatchObject({
      id: "mes_ventes",
      organization: { type: "subdirs", fixed_subdirs: ["mes_ventes.clients"] },
    });
  });
});
```

- [ ] **Step 1.2 : Vérifier que les tests échouent (module non trouvé)**

```bash
cd packages/referentiel-cli && npm test
```
Attendu : erreur `Cannot find module '../src/commands/export-frontmatters.js'`

---

## Task 2 : Installer les dépendances et implémenter export-frontmatters

**Files:**
- Modify: `packages/referentiel-cli/package.json`
- Create: `packages/referentiel-cli/src/commands/export-frontmatters.ts`

- [ ] **Step 2.1 : Ajouter les dépendances**

Dans `packages/referentiel-cli/package.json`, ajouter dans `"dependencies"` :
```json
"gray-matter": "^4.0.3",
"js-yaml": "^4.1.0"
```
Et dans `"devDependencies"` :
```json
"@types/js-yaml": "^4.0.9"
```

```bash
cd packages/referentiel-cli && npm install
```

- [ ] **Step 2.2 : Créer le fichier de la commande**

`packages/referentiel-cli/src/commands/export-frontmatters.ts` :
```typescript
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve, join } from "node:path";
import matter from "gray-matter";
import { dump } from "js-yaml";

export type ExportFrontmattersOptions = {
  output?: string;
  referentielRoot?: string;
};

function defaultReferentielRoot(): string {
  return resolve(process.cwd(), "packages", "referentiel");
}

export async function runExportFrontmatters(
  opts: ExportFrontmattersOptions = {}
): Promise<void> {
  const referentielRoot = resolve(
    opts.referentielRoot?.trim() || defaultReferentielRoot()
  );
  const classementDir = join(referentielRoot, "classement");
  const outputPath = resolve(
    opts.output?.trim() || join(referentielRoot, "referentiel.yaml")
  );

  const entries = readdirSync(classementDir)
    .filter((f) => f.endsWith(".md") && f !== "__index.md")
    .map((f) => {
      const raw = readFileSync(join(classementDir, f), "utf-8");
      return matter(raw).data as Record<string, unknown>;
    })
    .filter((d) => typeof d["id"] === "string")
    .sort((a, b) =>
      String(a["id"]).localeCompare(String(b["id"]))
    );

  const yaml = dump(entries, { lineWidth: -1, noRefs: true, quotingType: '"' });
  writeFileSync(outputPath, yaml, "utf-8");
  console.log(`✓ ${entries.length} entrées exportées → ${outputPath}`);
}
```

- [ ] **Step 2.3 : Lancer les tests**

```bash
cd packages/referentiel-cli && npm test
```
Attendu : 4 tests passent (✓)

- [ ] **Step 2.4 : Compiler**

```bash
cd packages/referentiel-cli && npm run build
```
Attendu : compilation sans erreur

- [ ] **Step 2.5 : Commit**

```bash
git add packages/referentiel-cli/package.json packages/referentiel-cli/package-lock.json packages/referentiel-cli/src/commands/export-frontmatters.ts packages/referentiel-cli/test/export-frontmatters.test.ts
git commit -m "feat(referentiel-cli): add export-frontmatters command"
```

---

## Task 3 : Enregistrer la commande dans cli.ts

**Files:**
- Modify: `packages/referentiel-cli/src/cli.ts`

- [ ] **Step 3.1 : Ajouter la commande dans cli.ts**

Ajouter après le bloc `program.command("push")...` et avant `program.parse()` :
```typescript
program
  .command("export-frontmatters")
  .description("Exporter tous les front matters vers referentiel.yaml")
  .option("--output <path>", "Chemin du fichier de sortie YAML")
  .option("--referentiel-root <path>", "Racine locale (défaut: ./packages/referentiel)")
  .action(async (opts: { output?: string; referentielRoot?: string }) => {
    const { runExportFrontmatters } = await import("./commands/export-frontmatters.js");
    await runExportFrontmatters(opts);
  });
```

- [ ] **Step 3.2 : Compiler et vérifier**

```bash
cd packages/referentiel-cli && npm run build && node dist/cli.js --help
```
Attendu : la commande `export-frontmatters` apparaît dans la liste

- [ ] **Step 3.3 : Commit**

```bash
git add packages/referentiel-cli/src/cli.ts
git commit -m "feat(referentiel-cli): register export-frontmatters in CLI"
```

---

## Task 4 : Réécrire mes_ventes.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md`
- Create: `packages/referentiel/classement/mes_ventes__factures_clients.md`
- Create: `packages/referentiel/classement/mes_ventes__modeles.md`
- Create: `packages/referentiel/classement/mes_ventes__modeles__contrats.md`
- Create: `packages/referentiel/classement/mes_ventes__modeles__devis_offres.md`
- Create: `packages/referentiel/classement/mes_ventes__clients.md`
- Create: `packages/referentiel/classement/mes_ventes__clients__nom_client.md`
- Create: `packages/referentiel/classement/mes_ventes__clients__nom_client__contrats.md`
- Create: `packages/referentiel/classement/mes_ventes__clients__nom_client__devis.md`

- [ ] **Step 4.1 : Réécrire mes_ventes.md**

```markdown
---
id: mes_ventes
folder_name: "Mes ventes"
path: "Mes ventes"
dynamic: false
option: core
required: true
description: "Relation commerciale sortante : factures clients, modèles, suivi client"
organization:
  type: subdirs
  fixed_subdirs:
    - mes_ventes.factures_clients
    - mes_ventes.modeles
    - mes_ventes.clients
---

# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures clients, modèles de contrat, de devis et d'offre, offres clients, suivi client.

```
Mes ventes/
├── Mes factures clients/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes modèles/
│   ├── Contrats/
│   └── Devis et offres/
└── Mes clients/
    └── [Nom du client]/
        ├── Contrats/
        ├── Devis/
        └── ...
```

**Ce qu'il faut retenir :**

- `Mes factures clients/` — factures émises, classées par mois. Voir [Mes factures clients](mes_ventes__factures_clients.md).
- `Mes modèles/` — gabarits réutilisables contrats et devis. Voir [Mes modèles](mes_ventes__modeles.md).
- `Mes clients/` — vue par client. Voir [Mes clients](mes_ventes__clients.md).
```

- [ ] **Step 4.2 : Créer mes_ventes__factures_clients.md**

```markdown
---
id: mes_ventes.factures_clients
folder_name: "Mes factures clients"
path: "Mes ventes/Mes factures clients"
parent: mes_ventes
dynamic: false
option: core
required: true
description: "Factures émises, classées par mois d'émission"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission de la facture"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero
      description: "numéro de la facture tel qu'il apparaît dans le logiciel"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Facture_Dupont_F2600003.pdf"
---

## `Mes factures clients/`

**Rôle :** factures **émises** par ton entreprise (pas les brouillons : une fois validée et envoyée, le PDF ou l'export comptable vit ici).

**Organisation :** un sous-dossier par mois d'émission utile, format `AAAA-MM` (`Mes factures clients/2026-03/`).

**Format des fichiers :** `[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission de la facture
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro de la facture tel qu'il apparaît dans le logiciel de facturation
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Facture_Dupont_F2600003.pdf`
```

- [ ] **Step 4.3 : Créer mes_ventes__modeles.md**

```markdown
---
id: mes_ventes.modeles
folder_name: "Mes modèles"
path: "Mes ventes/Mes modèles"
parent: mes_ventes
dynamic: false
option: core
required: true
description: "Gabarits réutilisables : contrats et devis/offres"
organization:
  type: subdirs
  fixed_subdirs:
    - mes_ventes.modeles.contrats
    - mes_ventes.modeles.devis_offres
---

## `Mes modèles/`

**Rôle :** gabarits réutilisables à dupliquer et adapter. Pas de document signé ni finalisé ici — uniquement les modèles types. Deux sous-dossiers fixes.

```
Mes modèles/
├── Contrats/       ← modèles de contrat et d'avenant
└── Devis et offres/  ← modèles de devis et de propositions commerciales
```
```

- [ ] **Step 4.4 : Créer mes_ventes__modeles__contrats.md**

```markdown
---
id: mes_ventes.modeles.contrats
folder_name: "Contrats"
path: "Mes ventes/Mes modèles/Contrats"
parent: mes_ventes.modeles
dynamic: false
option: core
required: true
description: "Modèles de contrat et d'avenant réutilisables"
organization:
  type: flat
file_naming:
  pattern: "modele-contrat_[objet]_v[N].[ext]"
  fields:
    - name: objet
      description: "type de contrat en mots séparés par des tirets (ex. maintenance-annuelle)"
    - name: N
      description: "version du gabarit (1, 2…)"
    - name: ext
      description: "extension du fichier (docx, odt…)"
  example: "modele-contrat_maintenance-annuelle_v2.docx"
---

### `Contrats/` (modèles)

**Rôle :** modèles de contrat et d'avenant à dupliquer. Pas de document signé ici.

**Format des fichiers :** `modele-contrat_[objet]_v[N].[ext]`

- `[objet]` — type de contrat en mots séparés par des tirets (`maintenance-annuelle`, `prestation-conseil`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-contrat_maintenance-annuelle_v2.docx`
```

- [ ] **Step 4.5 : Créer mes_ventes__modeles__devis_offres.md**

```markdown
---
id: mes_ventes.modeles.devis_offres
folder_name: "Devis et offres"
path: "Mes ventes/Mes modèles/Devis et offres"
parent: mes_ventes.modeles
dynamic: false
option: core
required: true
description: "Modèles de devis et de propositions commerciales réutilisables"
organization:
  type: flat
file_naming:
  pattern: "modele-devis_[objet]_v[N].[ext]"
  fields:
    - name: objet
      description: "type de prestation ou de format (ex. prestation-conseil)"
    - name: N
      description: "version du gabarit (1, 2…)"
    - name: ext
      description: "extension du fichier (docx, odt…)"
  example: "modele-devis_prestation-conseil_v1.docx"
---

### `Devis et offres/` (modèles)

**Rôle :** modèles de devis et d'offre commerciale à dupliquer. Pour un indép solo, un devis IS l'offre.

**Format des fichiers :** `modele-devis_[objet]_v[N].[ext]`

- `[objet]` — type de prestation (`prestation-conseil`, `formation-react`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-devis_prestation-conseil_v1.docx`
```

- [ ] **Step 4.6 : Créer mes_ventes__clients.md**

```markdown
---
id: mes_ventes.clients
folder_name: "Mes clients"
path: "Mes ventes/Mes clients"
parent: mes_ventes
dynamic: false
option: core
required: true
description: "Vue par client : contrats, devis et suivi libre"
organization:
  type: per_entity
  entity_subfolder: mes_ventes.clients.nom_client
---

## `Mes clients/`

**Rôle :** vue par client regroupant les documents directement liés à la relation commerciale. Chaque client dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par client, nom en français lisible (`[Nom du client]/`).

```
Mes clients/
└── [Nom du client]/
    ├── Contrats/
    ├── Devis/
    └── ...
```
```

- [ ] **Step 4.7 : Créer mes_ventes__clients__nom_client.md**

```markdown
---
id: mes_ventes.clients.nom_client
folder_name: "[Nom du client]"
path: "Mes ventes/Mes clients/[Nom du client]"
parent: mes_ventes.clients
dynamic: true
option: core
required: true
description: "Dossier par client : nom lisible en français"
organization:
  type: mixed
  fixed_subdirs:
    - mes_ventes.clients.nom_client.contrats
    - mes_ventes.clients.nom_client.devis
  free_subdirs: true
---

### `[Nom du client]/`

**Rôle :** regroupe les documents directement liés à un client : contrats signés, devis envoyés, notes de suivi, comptes-rendus.

Les sous-dossiers `Contrats/` et `Devis/` sont **imposés**. Le reste de l'organisation est libre par client.
```

- [ ] **Step 4.8 : Créer mes_ventes__clients__nom_client__contrats.md**

```markdown
---
id: mes_ventes.clients.nom_client.contrats
folder_name: "Contrats"
path: "Mes ventes/Mes clients/[Nom du client]/Contrats"
parent: mes_ventes.clients.nom_client
dynamic: false
option: core
required: true
description: "Contrats et avenants réels signés avec le client"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_Contrat_[Nom client]_[Numero-Revision].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission du contrat ou de l'avenant"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero-Revision
      description: "référence libre (numéro de contrat, objet, version…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-04_Contrat_Acme_C2026-01.pdf"
---

### `Contrats/` (client)

**Rôle :** tout contrat ou avenant une fois sorti du statut brouillon : versions partagées, PDF signé, scans. Structure plate.

**Format des fichiers :** `[AAAA-MM]_Contrat_[Nom client]_[Numero-Revision].[ext]`

Avenant : `[AAAA-MM]_Avenant_[Nom client]_[Numero-Revision].[ext]`

**Exemple :** `2026-04_Contrat_Acme_C2026-01.pdf`
```

- [ ] **Step 4.9 : Créer mes_ventes__clients__nom_client__devis.md**

```markdown
---
id: mes_ventes.clients.nom_client.devis
folder_name: "Devis"
path: "Mes ventes/Mes clients/[Nom du client]/Devis"
parent: mes_ventes.clients.nom_client
dynamic: false
option: core
required: true
description: "Devis et propositions commerciales envoyés au client"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission du devis"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero
      description: "numéro du devis tel qu'il apparaît dans le logiciel"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Devis_Martin_D2600001.pdf"
---

### `Devis/` (client)

**Rôle :** propositions chiffrées et offres commerciales envoyées au client. Pour un indép solo, un devis IS l'offre. Structure plate.

**Format des fichiers :** `[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]`

**Exemple :** `2026-03_Devis_Martin_D2600001.pdf`
```

- [ ] **Step 4.10 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md packages/referentiel/classement/mes_ventes__*.md
git commit -m "feat(referentiel): split mes_ventes into per-folder md files"
```

---

## Task 5 : Réécrire mes_achats.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/mes_achats.md`
- Create: `packages/referentiel/classement/mes_achats__factures_fournisseurs.md`
- Create: `packages/referentiel/classement/mes_achats__fournisseurs.md`
- Create: `packages/referentiel/classement/mes_achats__fournisseurs__nom_fournisseur.md`

- [ ] **Step 5.1 : Réécrire mes_achats.md**

```markdown
---
id: mes_achats
folder_name: "Mes achats"
path: "Mes achats"
dynamic: false
option: core
required: true
description: "Relation commerciale entrante : factures fournisseurs, suivi fournisseurs"
organization:
  type: subdirs
  fixed_subdirs:
    - mes_achats.factures_fournisseurs
    - mes_achats.fournisseurs
---

# `Mes achats/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale entrante : factures fournisseurs, suivi fournisseurs.

```
Mes achats/
├── Mes factures fournisseurs/
│   ├── [AAAA-MM]/
│   └── ...
└── Mes fournisseurs/
    └── [Nom du fournisseur]/
        └── ...
```

**Ce qu'il faut retenir :**

- `Mes factures fournisseurs/` — factures reçues, classées par mois. Voir [Mes factures fournisseurs](mes_achats__factures_fournisseurs.md).
- `Mes fournisseurs/` — vue par fournisseur. Voir [Mes fournisseurs](mes_achats__fournisseurs.md).
```

- [ ] **Step 5.2 : Créer mes_achats__factures_fournisseurs.md**

```markdown
---
id: mes_achats.factures_fournisseurs
folder_name: "Mes factures fournisseurs"
path: "Mes achats/Mes factures fournisseurs"
parent: mes_achats
dynamic: false
option: core
required: true
description: "Factures reçues, classées par mois de réception"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission de la facture"
    - name: Nom fournisseur
      description: "nom du fournisseur, forme lisible"
    - name: Numero
      description: "numéro de la facture tel qu'il apparaît sur le document"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Facture_OVH_F2600042.pdf"
---

## `Mes factures fournisseurs/`

**Rôle :** factures **reçues** par ton entreprise. Un sous-dossier par mois de réception, format `AAAA-MM`.

**Format des fichiers :** `[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]`

**Exemple :** `2026-03_Facture_OVH_F2600042.pdf`
```

- [ ] **Step 5.3 : Créer mes_achats__fournisseurs.md**

```markdown
---
id: mes_achats.fournisseurs
folder_name: "Mes fournisseurs"
path: "Mes achats/Mes fournisseurs"
parent: mes_achats
dynamic: false
option: core
required: true
description: "Vue par fournisseur : contrats, polices, attestations"
organization:
  type: per_entity
  entity_subfolder: mes_achats.fournisseurs.nom_fournisseur
---

## `Mes fournisseurs/`

**Rôle :** vue par fournisseur regroupant les documents liés à la relation. Chaque fournisseur a son propre sous-dossier.

**Organisation :** un sous-dossier par fournisseur, nom en français lisible. L'organisation interne est libre.
```

- [ ] **Step 5.4 : Créer mes_achats__fournisseurs__nom_fournisseur.md**

```markdown
---
id: mes_achats.fournisseurs.nom_fournisseur
folder_name: "[Nom du fournisseur]"
path: "Mes achats/Mes fournisseurs/[Nom du fournisseur]"
parent: mes_achats.fournisseurs
dynamic: true
option: core
required: true
description: "Dossier par fournisseur : nom lisible en français"
organization:
  type: free
  free_subdirs: true
---

### `[Nom du fournisseur]/`

**Rôle :** regroupe les documents liés à un fournisseur : contrats, polices d'assurance, attestations, échanges de référence. Organisation interne libre.
```

- [ ] **Step 5.5 : Commit**

```bash
git add packages/referentiel/classement/mes_achats.md packages/referentiel/classement/mes_achats__*.md
git commit -m "feat(referentiel): split mes_achats into per-folder md files"
```

---

## Task 6 : Réécrire mon_social.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/mon_social.md`
- Create: `packages/referentiel/classement/mon_social__fiches_de_paie.md`
- Create: `packages/referentiel/classement/mon_social__dpae.md`
- Create: `packages/referentiel/classement/mon_social__modeles_contrat_travail.md`
- Create: `packages/referentiel/classement/mon_social__salaries.md`
- Create: `packages/referentiel/classement/mon_social__salaries__nom_salarie.md`
- Create: `packages/referentiel/classement/mon_social__salaries__nom_salarie__contrats.md`
- Create: `packages/referentiel/classement/mon_social__declarations_sociales.md`
- Create: `packages/referentiel/classement/mon_social__attestations_urssaf.md`

- [ ] **Step 6.1 : Réécrire mon_social.md**

```markdown
---
id: mon_social
folder_name: "Mon social"
path: "Mon social"
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Gestion du personnel : fiches de paie, DPAE, modèles contrat travail, suivi salarié"
organization:
  type: subdirs
  fixed_subdirs:
    - mon_social.fiches_de_paie
    - mon_social.dpae
    - mon_social.modeles_contrat_travail
    - mon_social.salaries
    - mon_social.declarations_sociales
    - mon_social.attestations_urssaf
---

# `Mon social/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Gestion du personnel : fiches de paie, DPAE, modèles de contrat de travail, suivi salarié.

```
Mon social/
├── Mes fiches de paie/
├── Mes DPAE/
├── Mes modèles de contrat de travail/
├── Mes salariés/
├── Mes déclarations sociales/
└── Mes attestations URSSAF/
```
```

- [ ] **Step 6.2 : Créer mon_social__fiches_de_paie.md**

```markdown
---
id: mon_social.fiches_de_paie
folder_name: "Mes fiches de paie"
path: "Mon social/Mes fiches de paie"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Bulletins de paie de tous les salariés, classés par mois"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Fiche-de-paie_[Nom salarié].[ext]"
  fields:
    - name: AAAA-MM
      description: "mois de la paie"
    - name: Nom salarié
      description: "nom du salarié, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_Fiche-de-paie_Dupont.pdf"
---

## `Mes fiches de paie/`

**Rôle :** bulletins de paie de tous les salariés. Un sous-dossier par mois d'émission, format `AAAA-MM`.

**Format des fichiers :** `[AAAA-MM]_Fiche-de-paie_[Nom salarié].[ext]`

**Exemple :** `2026-03_Fiche-de-paie_Dupont.pdf`
```

- [ ] **Step 6.3 : Créer mon_social__dpae.md**

```markdown
---
id: mon_social.dpae
folder_name: "Mes DPAE"
path: "Mon social/Mes DPAE"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Déclarations préalables à l'embauche, structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_DPAE_[Nom salarié].[ext]"
  fields:
    - name: AAAA-MM
      description: "date de la déclaration"
    - name: Nom salarié
      description: "nom du salarié concerné, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-04_DPAE_Martin.pdf"
---

## `Mes DPAE/`

**Rôle :** déclarations préalables à l'embauche transmises à l'URSSAF. Structure plate.

**Format des fichiers :** `[AAAA-MM]_DPAE_[Nom salarié].[ext]`

**Exemple :** `2026-04_DPAE_Martin.pdf`
```

- [ ] **Step 6.4 : Créer mon_social__modeles_contrat_travail.md**

```markdown
---
id: mon_social.modeles_contrat_travail
folder_name: "Mes modèles de contrat de travail"
path: "Mon social/Mes modèles de contrat de travail"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Gabarits de contrat de travail réutilisables (pas de documents signés)"
organization:
  type: flat
file_naming:
  pattern: "modele-contrat-travail_[objet]_v[N].[ext]"
  fields:
    - name: objet
      description: "type de contrat (cdi, cdd, alternance…)"
    - name: N
      description: "version du gabarit (1, 2…)"
    - name: ext
      description: "extension du fichier (docx, odt…)"
  example: "modele-contrat-travail_cdi_v1.docx"
---

## `Mes modèles de contrat de travail/`

**Rôle :** gabarits de contrat de travail à dupliquer et compléter. Pas de document signé ici. Les contrats signés vont dans `Mes salariés/[salarié]/Contrats/`.

**Format des fichiers :** `modele-contrat-travail_[objet]_vN.[ext]`

**Exemple :** `modele-contrat-travail_cdi_v1.docx`
```

- [ ] **Step 6.5 : Créer mon_social__salaries.md**

```markdown
---
id: mon_social.salaries
folder_name: "Mes salariés"
path: "Mon social/Mes salariés"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Vue par salarié : contrats signés et suivi individuel"
organization:
  type: per_entity
  entity_subfolder: mon_social.salaries.nom_salarie
---

## `Mes salariés/`

**Rôle :** vue par salarié. Chaque salarié a son sous-dossier avec `Contrats/` imposé et le reste libre.
```

- [ ] **Step 6.6 : Créer mon_social__salaries__nom_salarie.md**

```markdown
---
id: mon_social.salaries.nom_salarie
folder_name: "[Nom du salarié]"
path: "Mon social/Mes salariés/[Nom du salarié]"
parent: mon_social.salaries
dynamic: true
option: dirigeant-assimile-salarie
required: true
description: "Dossier par salarié : nom lisible en français"
organization:
  type: mixed
  fixed_subdirs:
    - mon_social.salaries.nom_salarie.contrats
  free_subdirs: true
---

### `[Nom du salarié]/`

Le sous-dossier `Contrats/` est **imposé**. Le reste est libre (courriers, suivi, avenants non-contractuels).
```

- [ ] **Step 6.7 : Créer mon_social__salaries__nom_salarie__contrats.md**

```markdown
---
id: mon_social.salaries.nom_salarie.contrats
folder_name: "Contrats"
path: "Mon social/Mes salariés/[Nom du salarié]/Contrats"
parent: mon_social.salaries.nom_salarie
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Contrats de travail et avenants signés du salarié"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_Contrat_[Nom salarié]_[Référence].[ext]"
  fields:
    - name: AAAA-MM
      description: "date de signature"
    - name: Nom salarié
      description: "nom du salarié, forme lisible"
    - name: Référence
      description: "type de contrat ou référence libre (CDI, CDD…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-01_Contrat_Dupont_CDI.pdf"
---

### `Contrats/` (salarié)

**Rôle :** contrats de travail et avenants signés. Structure plate.

Avenant : `[AAAA-MM]_Avenant_[Nom salarié]_[Référence].[ext]`

**Exemple :** `2026-01_Contrat_Dupont_CDI.pdf`
```

- [ ] **Step 6.8 : Créer mon_social__declarations_sociales.md**

```markdown
---
id: mon_social.declarations_sociales
folder_name: "Mes déclarations sociales"
path: "Mon social/Mes déclarations sociales"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "DSN mensuelles et bordereaux URSSAF, classés par année puis mois"
organization:
  type: chronological
  subfolder_pattern: "AAAA/AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_[Type].[ext]"
  fields:
    - name: AAAA-MM
      description: "mois de la déclaration"
    - name: Type
      description: "type de document : DSN, Bordereau-cotisations"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_DSN.pdf"
---

## `Mes déclarations sociales/`

**Rôle :** DSN mensuelles et bordereaux de cotisations URSSAF. Obligatoire pour tout dirigeant SASU.

**Organisation :** un sous-dossier par année (`[AAAA]/`), puis par mois (`[AAAA-MM]/`).

**Exemples :** `2026-03_DSN.pdf` / `2026-03_Bordereau-cotisations.pdf`
```

- [ ] **Step 6.9 : Créer mon_social__attestations_urssaf.md**

```markdown
---
id: mon_social.attestations_urssaf
folder_name: "Mes attestations URSSAF"
path: "Mon social/Mes attestations URSSAF"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Attestations de vigilance et relevés de situation URSSAF"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_[Type].[ext]"
  fields:
    - name: AAAA-MM
      description: "date de délivrance du document"
    - name: Type
      description: "type de document : Attestation-vigilance, Releve-situation"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_Attestation-vigilance.pdf"
---

## `Mes attestations URSSAF/`

**Rôle :** attestations de vigilance (exigées pour tout contrat > 5 000 €) et relevés de situation. Structure plate.

**Exemples :** `2026-03_Attestation-vigilance.pdf` / `2026-03_Releve-situation.pdf`
```

- [ ] **Step 6.10 : Commit**

```bash
git add packages/referentiel/classement/mon_social.md packages/referentiel/classement/mon_social__*.md
git commit -m "feat(referentiel): split mon_social into per-folder md files"
```

---

## Task 7 : Réécrire ma_fiscalite.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/ma_fiscalite.md`
- Create: `packages/referentiel/classement/ma_fiscalite__declarations_tva.md`
- Create: `packages/referentiel/classement/ma_fiscalite__liasses_fiscales.md`
- Create: `packages/referentiel/classement/ma_fiscalite__avis_imposition.md`
- Create: `packages/referentiel/classement/ma_fiscalite__avis_cfe.md`

- [ ] **Step 7.1 : Réécrire ma_fiscalite.md**

```markdown
---
id: ma_fiscalite
folder_name: "Ma fiscalité"
path: "Ma fiscalité"
dynamic: false
option: core
required: true
description: "Obligations fiscales : TVA, liasses fiscales, avis d'imposition, CFE"
organization:
  type: subdirs
  fixed_subdirs:
    - ma_fiscalite.declarations_tva
    - ma_fiscalite.liasses_fiscales
    - ma_fiscalite.avis_imposition
    - ma_fiscalite.avis_cfe
---

# `Ma fiscalité/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Obligations fiscales : déclarations de TVA, liasses fiscales, avis d'imposition, avis de CFE.
```

- [ ] **Step 7.2 : Créer ma_fiscalite__declarations_tva.md**

```markdown
---
id: ma_fiscalite.declarations_tva
folder_name: "Mes déclarations de TVA"
path: "Ma fiscalité/Mes déclarations de TVA"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Déclarations de TVA (CA3, CA12…), classées par mois"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Declaration-TVA.[ext]"
  fields:
    - name: AAAA-MM
      description: "période couverte par la déclaration"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_Declaration-TVA.pdf"
---

## `Mes déclarations de TVA/`

**Rôle :** déclarations CA3 (mensuelle/trimestrielle) ou CA12 (annuelle). Un sous-dossier par mois, format `AAAA-MM`.

**Format des fichiers :** `[AAAA-MM]_Declaration-TVA.[ext]`

**Exemple :** `2026-03_Declaration-TVA.pdf`
```

- [ ] **Step 7.3 : Créer ma_fiscalite__liasses_fiscales.md**

```markdown
---
id: ma_fiscalite.liasses_fiscales
folder_name: "Mes liasses fiscales"
path: "Ma fiscalité/Mes liasses fiscales"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Liasses fiscales annuelles, structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Liasse-fiscale.[ext]"
  fields:
    - name: AAAA
      description: "exercice fiscal concerné"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2025_Liasse-fiscale.pdf"
---

## `Mes liasses fiscales/`

**Rôle :** liasses fiscales annuelles (bilan, compte de résultat, annexes). Structure plate, une liasse par exercice.

**Exemple :** `2025_Liasse-fiscale.pdf`
```

- [ ] **Step 7.4 : Créer ma_fiscalite__avis_imposition.md**

```markdown
---
id: ma_fiscalite.avis_imposition
folder_name: "Mes avis d'imposition"
path: "Ma fiscalité/Mes avis d'imposition"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Avis d'imposition reçus (IR, IS…), structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Avis-imposition_[Type].[ext]"
  fields:
    - name: AAAA
      description: "année fiscale concernée"
    - name: Type
      description: "type d'impôt (IR, IS…)"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2025_Avis-imposition_IR.pdf"
---

## `Mes avis d'imposition/`

**Rôle :** avis d'imposition reçus (IR, IS…). Structure plate.

**Exemple :** `2025_Avis-imposition_IR.pdf`
```

- [ ] **Step 7.5 : Créer ma_fiscalite__avis_cfe.md**

```markdown
---
id: ma_fiscalite.avis_cfe
folder_name: "Mes avis de CFE"
path: "Ma fiscalité/Mes avis de CFE"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Avis de cotisation foncière des entreprises, structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Avis-CFE.[ext]"
  fields:
    - name: AAAA
      description: "année fiscale concernée"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2025_Avis-CFE.pdf"
---

## `Mes avis de CFE/`

**Rôle :** avis de cotisation foncière des entreprises. Structure plate, un avis par an.

**Exemple :** `2025_Avis-CFE.pdf`
```

- [ ] **Step 7.6 : Commit**

```bash
git add packages/referentiel/classement/ma_fiscalite.md packages/referentiel/classement/ma_fiscalite__*.md
git commit -m "feat(referentiel): split ma_fiscalite into per-folder md files"
```

---

## Task 8 : Réécrire ma_banque.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/ma_banque.md`
- Create: `packages/referentiel/classement/ma_banque__releves_bancaires.md`
- Create: `packages/referentiel/classement/ma_banque__releves_bancaires__nom_banque.md`
- Create: `packages/referentiel/classement/ma_banque__rib.md`

- [ ] **Step 8.1 : Réécrire ma_banque.md**

```markdown
---
id: ma_banque
folder_name: "Ma banque"
path: "Ma banque"
dynamic: false
option: core
required: true
description: "Trésorerie : relevés bancaires et RIB"
organization:
  type: subdirs
  fixed_subdirs:
    - ma_banque.releves_bancaires
    - ma_banque.rib
---

# `Ma banque/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Trésorerie : relevés bancaires et RIB.
```

- [ ] **Step 8.2 : Créer ma_banque__releves_bancaires.md**

```markdown
---
id: ma_banque.releves_bancaires
folder_name: "Mes relevés bancaires"
path: "Ma banque/Mes relevés bancaires"
parent: ma_banque
dynamic: false
option: core
required: true
description: "Relevés de compte bancaire, organisés par établissement puis par mois"
organization:
  type: per_entity
  entity_subfolder: ma_banque.releves_bancaires.nom_banque
---

## `Mes relevés bancaires/`

**Rôle :** relevés de compte bancaire reçus. Un sous-dossier par établissement, puis un sous-dossier par mois.

```
Mes relevés bancaires/
└── [Nom banque]/
    └── [AAAA-MM]/
```
```

- [ ] **Step 8.3 : Créer ma_banque__releves_bancaires__nom_banque.md**

```markdown
---
id: ma_banque.releves_bancaires.nom_banque
folder_name: "[Nom banque]"
path: "Ma banque/Mes relevés bancaires/[Nom banque]"
parent: ma_banque.releves_bancaires
dynamic: true
option: core
required: true
description: "Dossier par établissement bancaire, contenant les relevés mensuels"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Releve_[Nom-banque]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "mois couvert par le relevé"
    - name: Nom-banque
      description: "nom de la banque, forme lisible (Credit-Mutuel, BNP, Qonto…)"
    - name: Numero
      description: "numéro du relevé tel qu'il apparaît sur le document"
    - name: ext
      description: "extension du fichier (pdf, csv…)"
  example: "2026-03_Releve_Credit-Mutuel_003.pdf"
---

### `[Nom banque]/`

**Rôle :** relevés mensuels d'un établissement bancaire. Sous-dossiers chronologiques `[AAAA-MM]/`.

**Exemple :** `2026-03_Releve_Credit-Mutuel_003.pdf`
```

- [ ] **Step 8.4 : Créer ma_banque__rib.md**

```markdown
---
id: ma_banque.rib
folder_name: "Mes RIB"
path: "Ma banque/Mes RIB"
parent: ma_banque
dynamic: false
option: core
required: true
description: "RIB des comptes bancaires professionnels actifs, structure plate"
organization:
  type: flat
file_naming:
  pattern: "RIB_[Nom-banque]_[Compte].[ext]"
  fields:
    - name: Nom-banque
      description: "nom de la banque, forme lisible"
    - name: Compte
      description: "type ou libellé du compte si plusieurs chez la même banque — omettre si unique"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "RIB_Credit-Mutuel.pdf"
---

## `Mes RIB/`

**Rôle :** relevés d'identité bancaire des comptes professionnels actifs. Structure plate — un fichier par compte.

**Exemples :** `RIB_Credit-Mutuel.pdf` / `RIB_Qonto_Courant.pdf`
```

- [ ] **Step 8.5 : Commit**

```bash
git add packages/referentiel/classement/ma_banque.md packages/referentiel/classement/ma_banque__*.md
git commit -m "feat(referentiel): split ma_banque into per-folder md files"
```

---

## Task 9 : Réécrire mes_assurances.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/mes_assurances.md`
- Create: `packages/referentiel/classement/mes_assurances__rc_pro.md`
- Create: `packages/referentiel/classement/mes_assurances__mutuelle_prevoyance.md`
- Create: `packages/referentiel/classement/mes_assurances__assurance_locaux.md`

- [ ] **Step 9.1 : Réécrire mes_assurances.md**

```markdown
---
id: mes_assurances
folder_name: "Mes assurances"
path: "Mes assurances"
dynamic: false
option: assurances
required: false
description: "Couvertures assurantielles : RC Pro, mutuelle/prévoyance, locaux et matériel"
organization:
  type: subdirs
  fixed_subdirs:
    - mes_assurances.rc_pro
    - mes_assurances.mutuelle_prevoyance
    - mes_assurances.assurance_locaux
---

# `Mes assurances/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Couvertures assurantielles : RC professionnelle, mutuelle et prévoyance, assurance locaux et matériel.
```

- [ ] **Step 9.2 : Créer mes_assurances__rc_pro.md**

```markdown
---
id: mes_assurances.rc_pro
folder_name: "RC Pro"
path: "Mes assurances/RC Pro"
parent: mes_assurances
dynamic: false
option: assurances
required: false
description: "Polices, attestations et avis d'échéance RC professionnelle"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Assureur].[ext]"
  fields:
    - name: AAAA
      description: "année de validité du document"
    - name: Type
      description: "nature du document : Police, Attestation, Echeance, Resiliation"
    - name: Assureur
      description: "nom de la compagnie, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Attestation_Hiscox.pdf"
---

## `RC Pro/`

**Rôle :** responsabilité civile professionnelle — police en vigueur, attestations annuelles, avis d'échéance. Structure plate.

**Exemples :** `2026_Attestation_Hiscox.pdf` / `2026_Police_Hiscox.pdf`
```

- [ ] **Step 9.3 : Créer mes_assurances__mutuelle_prevoyance.md**

```markdown
---
id: mes_assurances.mutuelle_prevoyance
folder_name: "Mutuelle et prévoyance"
path: "Mes assurances/Mutuelle et prévoyance"
parent: mes_assurances
dynamic: false
option: assurances
required: false
description: "Polices et attestations mutuelle santé et prévoyance"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Assureur].[ext]"
  fields:
    - name: AAAA
      description: "année de validité du document"
    - name: Type
      description: "nature du document : Police, Attestation, Remboursement"
    - name: Assureur
      description: "nom de la compagnie, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Attestation_AlanSante.pdf"
---

## `Mutuelle et prévoyance/`

**Rôle :** mutuelle santé et prévoyance — police, attestations d'affiliation. Structure plate.

**Exemple :** `2026_Attestation_AlanSante.pdf`
```

- [ ] **Step 9.4 : Créer mes_assurances__assurance_locaux.md**

```markdown
---
id: mes_assurances.assurance_locaux
folder_name: "Assurance locaux et matériel"
path: "Mes assurances/Assurance locaux et matériel"
parent: mes_assurances
dynamic: false
option: assurances
required: false
description: "Polices et attestations assurance locaux professionnels et matériel"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Assureur].[ext]"
  fields:
    - name: AAAA
      description: "année de validité du document"
    - name: Type
      description: "nature du document : Police, Attestation, Echeance"
    - name: Assureur
      description: "nom de la compagnie, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Police_MMA.pdf"
---

## `Assurance locaux et matériel/`

**Rôle :** assurance des locaux professionnels et du matériel. Structure plate.

**Exemple :** `2026_Police_MMA.pdf`
```

- [ ] **Step 9.5 : Commit**

```bash
git add packages/referentiel/classement/mes_assurances.md packages/referentiel/classement/mes_assurances__*.md
git commit -m "feat(referentiel): split mes_assurances into per-folder md files"
```

---

## Task 10 : Réécrire mon_juridique.md + créer les fichiers enfants

**Files:**
- Modify: `packages/referentiel/classement/mon_juridique.md`
- Create: `packages/referentiel/classement/mon_juridique__statuts.md`
- Create: `packages/referentiel/classement/mon_juridique__kbis.md`
- Create: `packages/referentiel/classement/mon_juridique__pv_decisions.md`
- Create: `packages/referentiel/classement/mon_juridique__registres.md`
- Create: `packages/referentiel/classement/mon_juridique__registres__mouvements_titres.md`
- Create: `packages/referentiel/classement/mon_juridique__registres__decisions.md`
- Create: `packages/referentiel/classement/mon_juridique__baux_domiciliation.md`
- Create: `packages/referentiel/classement/mon_juridique__cgv_mentions_legales.md`
- Create: `packages/referentiel/classement/mon_juridique__marques_licences.md`

- [ ] **Step 10.1 : Réécrire mon_juridique.md**

```markdown
---
id: mon_juridique
folder_name: "Mon juridique"
path: "Mon juridique"
dynamic: false
option: core
required: true
description: "Entité juridique : statuts, K-bis, PV, registres, baux, CGV"
organization:
  type: subdirs
  fixed_subdirs:
    - mon_juridique.statuts
    - mon_juridique.kbis
    - mon_juridique.pv_decisions
    - mon_juridique.registres
    - mon_juridique.baux_domiciliation
    - mon_juridique.cgv_mentions_legales
    - mon_juridique.marques_licences
---

# `Mon juridique/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Entité juridique : statuts, K-bis, procès-verbaux d'assemblée générale.
```

- [ ] **Step 10.2 : Créer mon_juridique__statuts.md**

```markdown
---
id: mon_juridique.statuts
folder_name: "Mes statuts"
path: "Mon juridique/Mes statuts"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Statuts constitutifs et mises à jour successives"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Statuts_[Objet].[ext]"
  fields:
    - name: AAAA
      description: "année de signature ou d'enregistrement"
    - name: Objet
      description: "nature du document (constitution, modification-objet-social…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026_Statuts_constitution.pdf"
---

## `Mes statuts/`

**Rôle :** statuts constitutifs et leurs mises à jour. Structure plate.

**Exemple :** `2026_Statuts_constitution.pdf`
```

- [ ] **Step 10.3 : Créer mon_juridique__kbis.md**

```markdown
---
id: mon_juridique.kbis
folder_name: "Mes K-bis"
path: "Mon juridique/Mes K-bis"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Extraits K-bis, justificatifs d'immatriculation"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Kbis.[ext]"
  fields:
    - name: AAAA
      description: "année d'émission"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Kbis.pdf"
---

## `Mes K-bis/`

**Rôle :** extraits K-bis demandés ou reçus. Structure plate.

**Exemple :** `2026_Kbis.pdf`
```

- [ ] **Step 10.4 : Créer mon_juridique__pv_decisions.md**

```markdown
---
id: mon_juridique.pv_decisions
folder_name: "Mes PV et décisions"
path: "Mon juridique/Mes PV et décisions"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "PV d'AG et décisions de l'associé unique (SASU)"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Objet].[ext]"
  fields:
    - name: AAAA
      description: "année de la décision ou de l'assemblée"
    - name: Type
      description: "PV-AG ou Decision-AU"
    - name: Objet
      description: "objet principal (approbation-comptes, dividendes, nomination-gerant…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026_PV-AG_approbation-comptes.pdf"
---

## `Mes PV et décisions/`

**Rôle :** PV d'assemblée générale et décisions de l'associé unique (SASU). Structure plate.

**Exemples :** `2026_PV-AG_approbation-comptes.pdf` / `2026_Decision-AU_dividendes.pdf`
```

- [ ] **Step 10.5 : Créer mon_juridique__registres.md**

```markdown
---
id: mon_juridique.registres
folder_name: "Mes registres"
path: "Mon juridique/Mes registres"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Registres obligatoires SASU : mouvements de titres et décisions"
organization:
  type: subdirs
  fixed_subdirs:
    - mon_juridique.registres.mouvements_titres
    - mon_juridique.registres.decisions
---

## `Mes registres/`

**Rôle :** registres légalement obligatoires pour une SASU.

```
Mes registres/
├── Registre des mouvements de titres/
└── Registre des décisions/
```
```

- [ ] **Step 10.6 : Créer mon_juridique__registres__mouvements_titres.md**

```markdown
---
id: mon_juridique.registres.mouvements_titres
folder_name: "Registre des mouvements de titres"
path: "Mon juridique/Mes registres/Registre des mouvements de titres"
parent: mon_juridique.registres
dynamic: false
option: core
required: true
description: "Versions successives du registre légal des mouvements de titres"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Registre_Mouvements-titres.[ext]"
  fields:
    - name: AAAA
      description: "année de l'export ou du scan"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Registre_Mouvements-titres.pdf"
---

### `Registre des mouvements de titres/`

**Rôle :** exports ou scans annuels du registre des mouvements de titres. Structure plate.

**Exemple :** `2026_Registre_Mouvements-titres.pdf`
```

- [ ] **Step 10.7 : Créer mon_juridique__registres__decisions.md**

```markdown
---
id: mon_juridique.registres.decisions
folder_name: "Registre des décisions"
path: "Mon juridique/Mes registres/Registre des décisions"
parent: mon_juridique.registres
dynamic: false
option: core
required: true
description: "Versions successives du registre légal des décisions"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Registre_Decisions.[ext]"
  fields:
    - name: AAAA
      description: "année de l'export ou du scan"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Registre_Decisions.pdf"
---

### `Registre des décisions/`

**Rôle :** exports ou scans annuels du registre des décisions. Structure plate.

**Exemple :** `2026_Registre_Decisions.pdf`
```

- [ ] **Step 10.8 : Créer mon_juridique__baux_domiciliation.md**

```markdown
---
id: mon_juridique.baux_domiciliation
folder_name: "Mes baux et domiciliation"
path: "Mon juridique/Mes baux et domiciliation"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Baux commerciaux, sous-location, contrats de domiciliation"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Bailleur].[ext]"
  fields:
    - name: AAAA
      description: "année de signature du contrat"
    - name: Type
      description: "type de document : Bail-commercial, Domiciliation, Avenant, Quittance"
    - name: Bailleur
      description: "nom du bailleur ou de la société de domiciliation, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Domiciliation_Regus.pdf"
---

## `Mes baux et domiciliation/`

**Rôle :** baux commerciaux, contrats de sous-location, contrats de domiciliation. Structure plate.

**Exemple :** `2026_Domiciliation_Regus.pdf`
```

- [ ] **Step 10.9 : Créer mon_juridique__cgv_mentions_legales.md**

```markdown
---
id: mon_juridique.cgv_mentions_legales
folder_name: "Mes CGV et mentions légales"
path: "Mon juridique/Mes CGV et mentions légales"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "CGV, CGU, mentions légales, politique de confidentialité"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_v[N].[ext]"
  fields:
    - name: AAAA
      description: "année de la version"
    - name: Type
      description: "type de document : CGV, CGU, Mentions-legales, Politique-confidentialite"
    - name: N
      description: "numéro de version (1, 2…)"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_CGV_v2.pdf"
---

## `Mes CGV et mentions légales/`

**Rôle :** conditions générales de vente, CGU, mentions légales du site web, politique de confidentialité. Structure plate.

**Exemple :** `2026_CGV_v2.pdf`
```

- [ ] **Step 10.10 : Créer mon_juridique__marques_licences.md**

```markdown
---
id: mon_juridique.marques_licences
folder_name: "Mes marques et licences"
path: "Mon juridique/Mes marques et licences"
parent: mon_juridique
dynamic: false
option: core
required: false
description: "Dépôts de marque INPI, licences logicielles, cessions de droits d'auteur (optionnel)"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Objet].[ext]"
  fields:
    - name: AAAA
      description: "année du dépôt ou de la signature"
    - name: Type
      description: "type de document : Depot-marque, Licence, Cession-droits, Certificat"
    - name: Objet
      description: "nom de la marque, du logiciel ou de l'œuvre, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Depot-marque_NomDeMarque.pdf"
---

## `Mes marques et licences/`

> **Dossier optionnel** — utile pour les indépendants du numérique, du créatif ou de la tech.

**Rôle :** dépôts de marque INPI, licences logicielles, cessions de droits d'auteur. Structure plate.

**Exemples :** `2026_Depot-marque_NomDeMarque.pdf` / `2026_Licence_Figma.pdf`
```

- [ ] **Step 10.11 : Commit**

```bash
git add packages/referentiel/classement/mon_juridique.md packages/referentiel/classement/mon_juridique__*.md
git commit -m "feat(referentiel): split mon_juridique into per-folder md files"
```

---

## Task 11 : Réécrire archives.md + créer le fichier enfant

**Files:**
- Modify: `packages/referentiel/classement/archives.md`
- Create: `packages/referentiel/classement/archives__annee.md`

- [ ] **Step 11.1 : Réécrire archives.md**

```markdown
---
id: archives
folder_name: "Archives"
path: "Archives"
dynamic: false
option: core
required: true
description: "Années closes : archives annuelles compressées avec manifest"
organization:
  type: per_entity
  entity_subfolder: archives.annee
---

# `Archives/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Années closes : archives annuelles compressées avec manifest.

```
Archives/
├── 2024/
│   ├── mes_ventes_2024.zip
│   └── manifest.md
└── 2023/
    └── ...
```

Le détail des règles d'archivage est dans [Règles d'archivage](../regles-archivage.md).
```

- [ ] **Step 11.2 : Créer archives__annee.md**

```markdown
---
id: archives.annee
folder_name: "[AAAA]"
path: "Archives/[AAAA]"
parent: archives
dynamic: true
option: core
required: true
description: "Dossier d'archive pour une année close : fichiers compressés + manifest"
organization:
  type: flat
file_naming:
  pattern: "[dossier-racine]_[AAAA].[ext]"
  fields:
    - name: dossier-racine
      description: "nom du dossier racine archivé, en minuscules avec tirets (mes_ventes, ma_banque…)"
    - name: AAAA
      description: "année archivée"
    - name: ext
      description: "format de compression (zip, tar.gz…)"
  example: "mes_ventes_2024.zip"
special_files:
  - name: manifest.md
    description: "liste des fichiers archivés et leur état (voir regles-archivage.md)"
---

### `[AAAA]/`

**Rôle :** dossier d'archive pour une année close. Contient un fichier compressé par dossier racine et un `manifest.md`.

**Exemple :** `Archives/2024/mes_ventes_2024.zip`
```

- [ ] **Step 11.3 : Commit**

```bash
git add packages/referentiel/classement/archives.md packages/referentiel/classement/archives__annee.md
git commit -m "feat(referentiel): split archives into per-folder md files"
```

---

## Task 12 : Générer referentiel.yaml

**Files:**
- Create: `packages/referentiel/referentiel.yaml`

- [ ] **Step 12.1 : Builder le CLI**

```bash
cd packages/referentiel-cli && npm run build
```
Attendu : compilation sans erreur

- [ ] **Step 12.2 : Lancer la génération**

```bash
node packages/referentiel-cli/dist/cli.js export-frontmatters
```
Attendu : `✓ N entrées exportées → packages/referentiel/referentiel.yaml`

Vérifier que N correspond au nombre de fichiers `.md` créés (hors `__index.md`).

- [ ] **Step 12.3 : Vérifier le contenu**

```bash
head -40 packages/referentiel/referentiel.yaml
```
Attendu : liste YAML commençant par `- id: archives` (premier dans l'ordre alphabétique), avec tous les champs du schéma.

- [ ] **Step 12.4 : Commit final**

```bash
git add packages/referentiel/referentiel.yaml
git commit -m "feat(referentiel): generate referentiel.yaml from front matters"
```
