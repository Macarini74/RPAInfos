# System Information Capture Project

## Description

This Python project captures and displays detailed information about the system, including:

- Machine User
- Model and Manufacturer
- Operating System
- RAM (DDR type and Size)
- Processor

Additionally, the captured data is stored in a local SQLite database.

## Requirements

- Python 3.x
- Libraries: `os`, `platform`, `psutil`, `sqlite3`

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/RPAInfos.git
    ```
2. Navigate to the project directory:
    ```bash
    cd RPAInfos
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script to capture system information and store it in the SQLite database:
```bash
python infoMaq.py
