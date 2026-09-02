# security-scanner

A command-line tool that reads a source file and asks Google Gemini to report the
security vulnerabilities in it — the vulnerability type, why it is exploitable, the
impact, and a fixed version of the code.

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
```

Copy the example environment file and add your key from
[Google AI Studio](https://aistudio.google.com/apikey):

```bash
cp .env.example .env
```

```
GOOGLE_API_KEY=your-api-key-here
```

## Usage

```bash
python scanner.py vulnerable.py
```

Scan several files at once:

```bash
python scanner.py src/auth.py src/db.py
```

Use a different model:

```bash
python scanner.py --model gemini-2.5-pro vulnerable.py
```

| Option | Description |
| --- | --- |
| `paths` | One or more files to scan |
| `--model` | Gemini model to use (default `gemini-2.5-flash`, or `$GEMINI_MODEL`) |

Exit code is `0` when every file scanned cleanly and `1` if any scan failed.

## Files

| File | Purpose |
| --- | --- |
| `scanner.py` | The scanner |
| `vulnerable.py` | Insecure sample code, used to check the scanner reports real findings |
| `.env.example` | Template for the required environment variables |

## Notes

`vulnerable.py` contains hardcoded credentials, SQL injection, command injection and
path traversal on purpose. It is test input — never import it or run it as part of an
application.

Findings come from a language model. Treat them as a first pass that points you at
areas to review, not as a substitute for a real audit.
