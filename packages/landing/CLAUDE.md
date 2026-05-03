# landing

Site vitrine — SPA statique React.

## Stack

- React 19, TypeScript
- Vite 7, Tailwind CSS 3, shadcn/ui (Radix)
- Routing : react-router-dom
- Tests : vitest + @testing-library/react

## Commandes

```bash
npm run dev                             # serveur dev
npm run build                           # build production
npm test                                # vitest run
npm run lint                            # eslint
```

## Layout

```
src/
  components/
    landing/         composants spécifiques à la landing
    ui/              composants shadcn/ui (générés, ne pas modifier à la main)
  hooks/             hooks React custom
  lib/               utilitaires (cn, etc.)
  pages/             pages routées
  test/              tests
```

## Conventions

- Composants dans `components/landing/`, un fichier par composant
- Ne pas modifier `components/ui/` directement — utiliser `npx shadcn-ui@latest add <component>`
- Styling : classes Tailwind, pas de CSS custom sauf cas exceptionnel
- Pages dans `pages/`, une par route
