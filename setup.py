#!/usr/bin/env python3
import os
from pathlib import Path

BASE_DIR = Path.home() / ".artfetch"

def main():
    print("Setting up base framework...")
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    display_script = BASE_DIR / "display.sh"

    display_script.write_text(r'''#!/bin/bash
# Usage: ~/.artfetch/display.sh [DIRECTORY]
TARGET_DIR="${1:-$HOME/.artfetch}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Directory not found: $TARGET_DIR"
    exit 1
fi

FILE=$(find "$TARGET_DIR" -type f \( -name "*.ansi" -o -name "*.txt" \) | shuf -n 1)

if [ -n "$FILE" ]; then
    DISPLAY_NAME=$(head -n 1 "$FILE")

    echo ""
    echo "$DISPLAY_NAME"
    echo ""

    tail -n +2 "$FILE"

    echo ""
fi
''')
    display_script.chmod(0o755)
    print(f"Display script successfully updated.")

if __name__ == "__main__":
    main()
    