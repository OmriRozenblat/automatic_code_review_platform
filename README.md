# Automatic Code Review Platform

Local POC for an automatic Python code review platform.

The system exposes a FastAPI server, receives scan requests through an API, reviews Python code using a local Ollama model, stores results in SQLite, and allows fetching results later by scan ID.

Everything runs locally. No cloud services are used.

## Features

* Submit Python files for review.
* Review code using predefined rules.
* Add extra rules per scan from the CLI.
* Fetch scan results asynchronously.
* Store results in a local SQLite database.
* Reuse existing scan results when possible.
* Limit the number of parallel scans.
* Delete expired scan results automatically.

## Default Rules

The default rules are stored in:

```text
scan/default_rules.txt
```

Initial rules:

```text
All variables have meaningful names
docstring of function reflects the actual code logic
```

## Requirements

* Python 3.11+
* Ollama installed locally
* Required Python packages from `requirements.txt`

Pull the configured Ollama model, for example:

```bash
ollama pull qwen2.5-coder:7b
```

## Installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Configuration is in `config.json`.

Example:

```json
{
  "API_BASE_URL": "http://127.0.0.1:8000",
  "max_parallel_scans": 5,
  "scan_ttl_minutes": 1440,
  "delete_interval_minutes": 1440,

  "model": {
    "provider": "ollama",
    "name": "qwen2.5-coder:7b",
    "temperature": 0,
    "num_predict": 100
  }
}
```

For 24-hour retention:

```json
"scan_ttl_minutes": 1440,
"delete_interval_minutes": 1440
```

## Run the Server

From the project root (from the venv):

```bash
uvicorn API.api:app --reload
```

API docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Use the CLI
Open a different terminal from project root.
The CLI client is:

```text
acr.py
```

Show help:

```bash
python acr.py --help
```

Submit a scan using the default file from `file_to_scan/`:

```bash
python acr.py scan
```

Submit a specific file:

```bash
python acr.py scan --path file_to_scan/example.py
```

Submit with extra rules:

```bash
python acr.py scan --path file_to_scan/example.py --add-rules "code must have a print" "code must not use global variables"
```

Fetch results:

```bash
python acr.py fetch --id 1
```

## Notes

* Ollama must be running before submitting scans.
* `acr.py` is only a client over the API.
* The review logic runs through the FastAPI server.
* Results are stored in local SQLite.
* Expired scans are deleted according to the configuration.


## Troubleshooting

If the model does not respond, make sure Ollama is running and that the configured model was pulled successfully.

If the database becomes inconsistent during development or after a crash, you can delete the local database file and run the program again. The database will be recreated automatically on the next run.

## Disclaimer

AI model responses may not always be fully accurate.
For best results, use clear and specific rules.
