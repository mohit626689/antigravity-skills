#!/usr/bin/env bash
# Render a Company Storybook HTML file into a print-ready PDF using headless Chrome/Chromium.
# Usage: ./render_book_pdf.sh <path/to/book.html> <path/to/output.pdf>
set -euo pipefail

IN="${1:?usage: render_book_pdf.sh <input.html> <output.pdf>}"
OUT="${2:?usage: render_book_pdf.sh <input.html> <output.pdf>}"

# Resolve absolute path for proper file:// URL
ABS_IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
OUT_DIR="$(dirname "$OUT")"
mkdir -p "$OUT_DIR"
ABS_OUT="$(cd "$OUT_DIR" 2>/dev/null && pwd)/$(basename "$OUT")"

# Find Chrome / Chromium across macOS and Linux
CANDIDATES=(
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  "/Applications/Chromium.app/Contents/MacOS/Chromium"
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
  "google-chrome"
  "google-chrome-stable"
  "chromium"
  "chromium-browser"
)

CHROME=""
for c in "${CANDIDATES[@]}"; do
  if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then
    CHROME="$c"
    break
  fi
done

if [ -z "$CHROME" ]; then
  echo "ERROR: Could not find Google Chrome or Chromium. Install Chrome and retry." >&2
  exit 1
fi

echo "📖 Rendering Company Storybook to PDF with: $CHROME"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --allow-file-access-from-files \
  --print-to-pdf="$ABS_OUT" "file://$ABS_IN"

echo "✅ Publication-ready Company Storybook PDF compiled: $ABS_OUT"
