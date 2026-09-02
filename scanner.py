"""Scan source files for security vulnerabilities using Google Gemini."""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"
MAX_BYTES = 200_000

PROMPT = """You are a security expert. Analyze this code for vulnerabilities.

For each issue, provide:
1. Vulnerability type
2. Why it is vulnerable (1 sentence)
3. Impact (1 sentence)
4. Secure code fix

Be concise. If the code has no vulnerabilities, say so and stop.

File: {name}

Code:
{code}
"""


def read_source(path):
    """Return the text of path, or exit with a clear message."""
    if not path.is_file():
        sys.exit(f"Not a file: {path}")

    size = path.stat().st_size
    if size == 0:
        sys.exit(f"File is empty: {path}")
    if size > MAX_BYTES:
        sys.exit(f"File is too large ({size:,} bytes, limit {MAX_BYTES:,}): {path}")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        sys.exit(f"File is not UTF-8 text: {path}")


def scan(client, model, path):
    """Send one file to the model and print the findings."""
    code = read_source(path)
    prompt = PROMPT.format(name=path.name, code=code)

    response = client.models.generate_content(model=model, contents=prompt)

    print(f"\n=== {path} ===")
    print(response.text.strip() if response.text else "(no response from model)")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="scanner",
        description="Scan source files for security vulnerabilities using Google Gemini.",
    )
    parser.add_argument("paths", nargs="+", type=Path, help="file(s) to scan")
    parser.add_argument(
        "--model",
        default=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        help=f"Gemini model to use (default: {DEFAULT_MODEL})",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key.")

    client = genai.Client(api_key=api_key)

    failed = False
    for path in args.paths:
        try:
            scan(client, args.model, path)
        except SystemExit:
            raise
        except Exception as exc:
            print(f"\n=== {path} ===", file=sys.stderr)
            print(f"Scan failed: {exc}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
