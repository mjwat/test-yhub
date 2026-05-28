#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLURE_DIR="$ROOT_DIR/allure"
RESULTS_DIR="$ALLURE_DIR/results"
REPORT_DIR="$ALLURE_DIR/report"
REPORT_INDEX="$REPORT_DIR/index.html"
HISTORY_CACHE_DIR="$ALLURE_DIR/history"
CATEGORIES_FILE="$ALLURE_DIR/categories.json"
OPEN_REPORT=false
PYTEST_ARGS=()

if [[ -x "$ROOT_DIR/venv/bin/python3" ]]; then
  PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/venv/bin/python3}"
elif [[ -x "$ROOT_DIR/venv/bin/python" ]]; then
  PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/venv/bin/python}"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --open)
      OPEN_REPORT=true
      shift
      ;;
    *)
      PYTEST_ARGS+=("$1")
      shift
      ;;
  esac
done

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "$PYTHON_BIN is not installed or not available in PATH." >&2
  exit 1
fi

if ! command -v allure >/dev/null 2>&1; then
  echo "Allure CLI is not installed or not available in PATH." >&2
  exit 1
fi

rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

set +e
if [[ ${#PYTEST_ARGS[@]} -gt 0 ]]; then
  "$PYTHON_BIN" -m pytest --alluredir="$RESULTS_DIR" "${PYTEST_ARGS[@]}"
else
  "$PYTHON_BIN" -m pytest --alluredir="$RESULTS_DIR"
fi
PYTEST_EXIT_CODE=$?
set -e

if [[ -d "$HISTORY_CACHE_DIR/history" ]]; then
  mkdir -p "$RESULTS_DIR/history"
  cp -R "$HISTORY_CACHE_DIR/history/." "$RESULTS_DIR/history/"
fi

if [[ -f "$CATEGORIES_FILE" ]]; then
  cp "$CATEGORIES_FILE" "$RESULTS_DIR/categories.json"
fi

allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean --single-file

if [[ -d "$REPORT_DIR/history" ]]; then
  rm -rf "$HISTORY_CACHE_DIR"
  mkdir -p "$HISTORY_CACHE_DIR/history"
  cp -R "$REPORT_DIR/history/." "$HISTORY_CACHE_DIR/history/"
fi

if [[ "$OPEN_REPORT" == true ]]; then
  if [[ ! -f "$REPORT_INDEX" ]]; then
    echo "Generated report index file was not found: $REPORT_INDEX" >&2
    exit 1
  fi

  case "$(uname -s)" in
    Darwin)
      open "$REPORT_INDEX"
      ;;
    Linux)
      xdg-open "$REPORT_INDEX"
      ;;
    *)
      echo "Report generated at: $REPORT_INDEX"
      echo "Open the file manually on this platform."
      ;;
  esac
fi

exit "$PYTEST_EXIT_CODE"
