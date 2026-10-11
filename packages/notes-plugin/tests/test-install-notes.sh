#!/usr/bin/env bash
# Tests de hooks/install-notes.sh, en bash pur (uname et curl simulés).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT="$HERE/../hooks/install-notes.sh"
FIXTURE="$HERE/fixtures/releases.json"
ROOT=$(mktemp -d)
FAILFILE="$ROOT/failures"
: > "$FAILFILE"
trap 'rm -rf "$ROOT"' EXIT

fail() { echo "  FAIL $1"; echo x >> "$FAILFILE"; }
assert_eq() { # attendu obtenu message
  if [ "$1" = "$2" ]; then echo "  ok   $3"; else fail "$3 (attendu: '$1', obtenu: '$2')"; fi
}
assert_file() { # test-flag chemin message
  if [ "$1" "$2" ]; then echo "  ok   $3"; else fail "$3 ($1 $2)"; fi
}

# Prépare un test isolé : dossier temporaire, uname/curl simulés, environnement
setup() {
  tmp=$(mktemp -d "$ROOT/t.XXXXXX")
  mkdir -p "$tmp/fakebin" "$tmp/data"
  CALLS="$tmp/calls"; : > "$CALLS"
  FAKE_BINARY="$tmp/binary"; printf 'NOUVEAU' > "$FAKE_BINARY"
  FAKE_API_JSON=$(cat "$FIXTURE")
  FAKE_UNAME_S=Linux; FAKE_UNAME_M=x86_64
  FAKE_DOWNLOAD_FAIL=0; FAKE_API_FAIL=0
  export CALLS FAKE_BINARY FAKE_API_JSON FAKE_UNAME_S FAKE_UNAME_M FAKE_DOWNLOAD_FAIL FAKE_API_FAIL
  cat > "$tmp/fakebin/uname" <<'U'
#!/usr/bin/env bash
case "$1" in -s) printf '%s\n' "$FAKE_UNAME_S" ;; -m) printf '%s\n' "$FAKE_UNAME_M" ;; esac
U
  cat > "$tmp/fakebin/curl" <<'C'
#!/usr/bin/env bash
out=""; prev=""; last=""
for a in "$@"; do
  [ "$prev" = "-o" ] && out="$a"
  prev="$a"; last="$a"
done
printf '%s\n' "$last" >> "$CALLS"
if [ -n "$out" ]; then
  [ "${FAKE_DOWNLOAD_FAIL:-0}" = 1 ] && exit 22
  cp "$FAKE_BINARY" "$out"
else
  [ "${FAKE_API_FAIL:-0}" = 1 ] && exit 6
  printf '%s' "$FAKE_API_JSON"
fi
C
  chmod +x "$tmp/fakebin/uname" "$tmp/fakebin/curl"
  export PATH="$tmp/fakebin:$PATH" CLAUDE_PLUGIN_DATA="$tmp/data"
}

run() { bash "$SCRIPT" >"$tmp/out" 2>"$tmp/err"; RC=$?; }
assert_silent() { assert_eq "" "$(cat "$tmp/out")$(cat "$tmp/err")" "stdout et stderr vides"; }
downloads() { grep -c '/notes-linux$\|/notes-macos-arm64$' "$CALLS"; }
old_install() {
  printf 'ANCIEN' > "$tmp/data/notes"; chmod +x "$tmp/data/notes"
  printf '%s\n' "${1:-notes-cli/0.20261010.1}" > "$tmp/data/version"
}

test_linux_fresh() {
  setup; run
  assert_eq 0 "$RC" "sort en 0"
  assert_file -x "$tmp/data/notes" "notes exécutable"
  assert_eq NOUVEAU "$(cat "$tmp/data/notes")" "contenu du binaire"
  assert_eq notes-cli/0.20261011.1 "$(cat "$tmp/data/version")" "version"
  case "$(tail -n1 "$CALLS")" in *notes-cli/0.20261011.1/notes-linux) r=ok ;; *) r=ko ;; esac
  assert_eq ok "$r" "URL se termine par notes-cli/0.20261011.1/notes-linux"
  assert_silent
}

test_darwin_arm64() {
  setup; FAKE_UNAME_S=Darwin; FAKE_UNAME_M=arm64; export FAKE_UNAME_S FAKE_UNAME_M
  run
  assert_eq 0 "$RC" "sort en 0"
  case "$(tail -n1 "$CALLS")" in */notes-macos-arm64) r=ok ;; *) r=ko ;; esac
  assert_eq ok "$r" "URL se termine par /notes-macos-arm64"
  assert_silent
}

test_up_to_date() {
  setup; old_install notes-cli/0.20261011.1; run
  assert_eq 0 "$RC" "sort en 0"
  assert_eq 0 "$(downloads)" "aucun téléchargement"
  assert_eq ANCIEN "$(cat "$tmp/data/notes")" "binaire inchangé"
  assert_silent
}

test_older_installed() {
  setup; old_install; run
  assert_eq 0 "$RC" "sort en 0"
  assert_eq NOUVEAU "$(cat "$tmp/data/notes")" "binaire remplacé"
  assert_eq notes-cli/0.20261011.1 "$(cat "$tmp/data/version")" "version remplacée"
  assert_silent
}

test_api_down() {
  setup; old_install; FAKE_API_FAIL=1; export FAKE_API_FAIL; run
  assert_eq 0 "$RC" "sort en 0"
  assert_eq ANCIEN "$(cat "$tmp/data/notes")" "ancien binaire intact"
  assert_silent
}

test_download_fails() {
  setup; old_install; FAKE_DOWNLOAD_FAIL=1; export FAKE_DOWNLOAD_FAIL; run
  assert_eq 0 "$RC" "sort en 0"
  assert_eq ANCIEN "$(cat "$tmp/data/notes")" "ancien binaire intact"
  assert_eq notes-cli/0.20261010.1 "$(cat "$tmp/data/version")" "ancienne version intacte"
  assert_eq "notes version" "$(ls "$tmp/data" | tr '\n' ' ' | sed 's/ $//')" "aucun fichier temporaire"
  assert_eq "" "$(ls -A "$tmp/data" | grep '^\.' || true)" "aucun fichier caché"
  assert_silent
}

test_unsupported_os() {
  local combo
  for combo in "Linux aarch64" "Darwin x86_64" "MINGW64_NT x86_64"; do
    setup
    FAKE_UNAME_S=${combo% *}; FAKE_UNAME_M=${combo#* }; export FAKE_UNAME_S FAKE_UNAME_M
    run
    assert_eq 0 "$RC" "$combo : sort en 0"
    assert_eq 0 "$(grep -c . "$CALLS")" "$combo : aucun appel curl"
    assert_silent
  done
}

test_no_notes_release() {
  setup
  FAKE_API_JSON=$(grep -v 'notes-cli' "$FIXTURE"); export FAKE_API_JSON
  run
  assert_eq 0 "$RC" "sort en 0"
  assert_eq 0 "$(downloads)" "aucun téléchargement"
  assert_eq "" "$(ls -A "$tmp/data")" "rien d'installé"
  assert_silent
}

for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  echo "$t"
  ( "$t" )
done

n=$(grep -c x "$FAILFILE")
if [ "$n" -gt 0 ]; then echo "$n échec(s)"; exit 1; fi
echo "tous les tests passent"
