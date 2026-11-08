# Preview hook for .github/scripts/render-previews.sh: bat renders a Rust sample
# with each variant.
# shellcheck shell=bash
name=bat

setup() {
  # A throwaway config and cache keep the user's own bat untouched.
  export BAT_CONFIG_DIR="$work/config" BAT_CACHE_DIR="$work/cache"
  mkdir -p "$BAT_CONFIG_DIR/themes"
  cp "$root"/themes/*.tmTheme "$BAT_CONFIG_DIR/themes/"
  bat cache --build >/dev/null
}

capture() {
  # A missing fixture gives empty output, which render-previews.sh rejects.
  # Run from the fixtures directory so the header shows a relative path.
  (cd "$root/scripts/fixtures" && bat --theme "kanagawa-$1" --color=always \
    --style=full --paging=never --terminal-width 80 sample.rs) >"$2"
}
