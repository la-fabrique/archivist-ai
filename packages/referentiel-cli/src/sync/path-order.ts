/** Trie les chemins relatifs : dossiers parents avant enfants (par profondeur), puis ordre lexicographique. */
export function orderedReferencePaths(paths: string[]): string[] {
  return [...paths].sort((a, b) => {
    const depth = (p: string) => p.split("/").length;
    const da = depth(a);
    const db = depth(b);
    if (da !== db) {
      return da - db;
    }
    return a < b ? -1 : a > b ? 1 : 0;
  });
}
