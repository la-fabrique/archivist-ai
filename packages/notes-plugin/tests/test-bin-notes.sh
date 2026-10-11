#!/usr/bin/env bash
# Tests de bin/notes (script relais), en bash pur.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT="$HERE/../bin/notes"
ROOT=$(mktemp -d)
FAILFILE="$ROOT/failures"
: > "$FAILFILE"
trap 'rm -rf "$ROOT"' EXIT

fail() { echo "  FAIL $1"; echo x >> "$FAILFILE"; }
assert_eq() { # attendu obtenu message
  if [ "$1" = "$2" ]; then echo "  ok   $3"; else fail "$3 (attendu: '$1', obtenu: '$2')"; fi
}
assert_contains() { # texte motif message
  case "$1" in *"$2"*) echo "  ok   $3" ;; *) fail "$3 (absent: '$2')" ;; esac
}

setup() {
  tmp=$(mktemp -d "$ROOT/t.XXXXXX")
  mkdir -p "$tmp/data"
}

# Faux binaire notes : affiche chaque argument entre crochets et sort en 3
fake_binary() { # dossier
  cat > "$1/notes" <<'B'
#!/usr/bin/env bash
for a in "$@"; do printf '[%s]\n' "$a"; done
exit 3
B
  chmod +x "$1/notes"
}

test_binary_present() {
  setup; fake_binary "$tmp/data"
  CLAUDE_PLUGIN_DATA="$tmp/data" bash "$SCRIPT" add idea "a b" --reply -x >"$tmp/out" 2>"$tmp/err"
  assert_eq 3 "$?" "code de sortie 3 propagé"
  assert_eq "$(printf '[add]\n[idea]\n[a b]\n[--reply]\n[-x]')" "$(cat "$tmp/out")" "arguments transmis à l'identique"
}

test_binary_absent() {
  local err
  setup
  CLAUDE_PLUGIN_DATA="$tmp/data" bash "$SCRIPT" add idea x >"$tmp/out" 2>"$tmp/err"
  assert_eq 127 "$?" "code de sortie 127"
  assert_eq "" "$(cat "$tmp/out")" "stdout vide"
  err=$(cat "$tmp/err")
  assert_contains "$err" "Redémarre ta session Claude Code" "message de redémarrage"
  assert_contains "$err" "$tmp/data/notes" "chemin data/notes"
  assert_contains "$err" "$tmp/data/version" "chemin data/version"
  assert_contains "$err" "https://github.com/la-fabrique/marketplace-ai/releases" "URL des releases"
}

test_default_data_dir_home() {
  setup; mkdir -p "$tmp/.claude/plugins/data/notes-archivist"
  fake_binary "$tmp/.claude/plugins/data/notes-archivist"
  env -u CLAUDE_PLUGIN_DATA -u CLAUDE_CONFIG_DIR HOME="$tmp" bash "$SCRIPT" hello >"$tmp/out" 2>"$tmp/err"
  assert_eq 3 "$?" "binaire trouvé sous HOME/.claude"
  assert_eq "[hello]" "$(cat "$tmp/out")" "argument transmis"
}

test_default_data_dir_config_dir() {
  setup; mkdir -p "$tmp/cfg/plugins/data/notes-archivist"
  fake_binary "$tmp/cfg/plugins/data/notes-archivist"
  env -u CLAUDE_PLUGIN_DATA HOME="$tmp/nohome" CLAUDE_CONFIG_DIR="$tmp/cfg" bash "$SCRIPT" hello >"$tmp/out" 2>"$tmp/err"
  assert_eq 3 "$?" "binaire trouvé sous CLAUDE_CONFIG_DIR"
  assert_eq "[hello]" "$(cat "$tmp/out")" "argument transmis"
}

for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  echo "$t"
  ( "$t" )
done

n=$(grep -c x "$FAILFILE")
if [ "$n" -gt 0 ]; then echo "$n échec(s)"; exit 1; fi
echo "tous les tests passent"
