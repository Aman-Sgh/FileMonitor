# File Integrity Monitor

A small Python project for learning more about file integrity monitoring and basic security concepts.

The tool keeps track of selected files using SHA-256 hashes and stores the information in a SQLite database. It can detect when files are modified, deleted or newly added.

## What it can do

- Scan a directory and its subdirectories
- Create a baseline of the files
- Detect modified, deleted and new files
- Store file information in SQLite
- Keep a history of detected changes
- Show the results through a simple CLI

## Requirements

- Python 3.14+
- Git

## Installation

Clone the repository:

```Terminal
git clone <repository-url>
cd file-integrity-monitor
```

Create a virtual environment:

```Terminal
python -m venv .venv
```

Activate the virtual environment:

```Terminal
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```Terminal
python -m pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` and set the directory you want to monitor.

Example:

```yaml
paths:
  - "C:\\FIM\\important"    # HERE CHANGE DIRECTORY

scan:
  recursive: true  #DO NOT TOUCH

hash:
  algorithm: sha256   #DO NOT TOUCH

logging:
  level: INFO   #DO NOT TOUCH
```

## Usage

# Run a scan:

```Terminal
python -m src.fim.cli scan
```

# Check the current status:

```Terminal
python -m src.fim.cli status
```

# List tracked files:

```Terminal
python -m src.fim.cli list
```

# View the change history:

```Terminal
python -m src.fim.cli history
```

## Example

After changing or deleting files, a scan can show:

```text
Scan completed.
Directory: C:\FIM\important

Modified:  1
Deleted:   1
New:       0
Unchanged: 1
```

The detected changes are stored in the SQLite database and can be viewed using the `history` command.

## Tests

The project uses pytest for testing.

Run all tests with:

```Terminal
python -m pytest
```

## Project Structure

```text
file-integrity-monitor/
├── src/
│   └── fim/
│       ├── __init__.py
│       ├── cli.py
│       ├── scanner.py
│       ├── hasher.py
│       ├── database.py
│       ├── monitor.py
│       └── config.py
├── tests/
│   ├── test_hasher.py
│   ├── test_scanner.py
│   ├── test_database.py
│   └── test_monitor.py
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Tech Stack

- Python
- SQLite
- SHA-256
- PyYAML
- pytest