# Automatic Code Review Platform

## Overview

Automatic Code Review Platform is a local AI-integrated code reviewer.

The platform allows the user to provide Python code and a set of review rules.
A local AI model then checks whether the code complies with each rule and stores the review result in a local database.

The project is designed as a proof of concept for asynchronous AI-based code review.

## Features

* Review Python code according to user-defined rules
* Run reviews using a configurable local AI model
* Store scan results in a local SQLite database
* Fetch previous scan results by scan ID
* Avoid duplicate scans by checking existing code/rules combinations
* Configure scan expiration time
* Configure the maximum number of scans running in parallel
* Configure prompts and model settings through a config file

## Requirements

Before running the project, make sure you have:

* Python 3 installed
* Ollama installed
* A supported Ollama model pulled locally
* Required Python packages installed

## Ollama Setup

This project uses Ollama as the local model provider.

First, make sure Ollama is installed and running.


```bash
ollama 
```

To pull a model, for example:

```bash
ollama pull qwen2.5-coder:7b
```

You can test the model manually with:

```bash
ollama run qwen2.5-coder:7b
```

Make sure the model name in your config file matches the model you pulled.

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

The platform can be configured through the config file.

Configurable values include:

* Maximum number of parallel scans
* Scan result expiration time
* AI model provider
* AI model name
* Model generation options
* System prompt
* User prompt template

Example configuration fields:

```json
{
  "max_parallel_scans": 5,
  "scan_ttl_minutes": 1440,
  "model": {
    "provider": "ollama",
    "name": "qwen2.5-coder:7b",
    "temperature": 0,
    "num_predict": 100
  }
}
```

## Running the Project

Run the main program:

```bash
python main.py
```

or, depending on your environment:

```bash
python3 main.py
```

After starting the program, follow the terminal instructions.


You will be able to:

* Submit a new scan
* Fetch existing scan results
* Quit the program

## Input File

When starting a scan, you can provide a direct path to the Python file you want to scan.

For example:

```text
C:/Users/paul_muadib/file.py
```

Alternatively, you can place the file inside the `file_to_scan` folder.
If no path is provided, the program will automatically scan the first file found in that folder.


## Basic Flow

1. Start Ollama.
2. Pull the model you want to use.
3. Install the project requirements.
4. Configure the config file.
5. Run `main.py`.
6. Submit code and review rules.
7. Receive a scan ID.
8. Fetch the result later using the scan ID.

Please note result will be None if model did not output a result yet.

## Notes

* The project currently focuses on Python code review.
* Scan results are stored locally in SQLite.
* Results expire after the configured time.
* If the same code and same rules were already scanned, the platform can return the existing scan instead of running the model again.
* For the proof of concept, scan requests may be rejected when the maximum number of parallel scans is reached.

## Troubleshooting

If the model does not respond, make sure Ollama is running and that the configured model was pulled successfully.

If the database becomes inconsistent during development or after a crash, you can delete the local database file and run the program again. The database will be recreated automatically on the next run.

## Disclaimer

AI model responses may not always be fully accurate.
For best results, use clear and specific rules.
