# File Processor

## Overview

The **File Processor** is a Django-based application designed to handle file reconciliation tasks. 
This application processes two CSV files (source and target), comparing their contents to identify discrepancies, 
missing records, and generate comprehensive reports.

## Features

- Upload and process CSV files.
- Compare records between source and target files.
- Identify missing records in both source and target files.
- Generate discrepancy reports with detailed information.
- RESTful API endpoints for file upload and report retrieval.

## Requirements

- Python 3.10 or higher
- Django 4.2 or higher
- Django REST Framework
- Pandas for data manipulation

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd file_processor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Ensure your database settings are configured in `file_processor/settings.py`.
   - Run the migrations:
   ```bash
   python manage.py migrate
   ```

5. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## Usage

### API Endpoints

1. **Upload Files**
   - **Endpoint:** `/api/v1/processor/upload/`
   - **Method:** `POST`
   - **Payload:**
     - `source_file`: (file) The source CSV file.
     - `target_file`: (file) The target CSV file.

2. **Generate Report**
   - **Endpoint:** `/api/v1/processor/report/`
   - **Method:** `GET`
   - **Query Parameters:**
     - `report_type`: (string) Type of report to generate (e.g., `json`, `html`, `csv`).

### Example Usage

To upload files, you can use a tool like Postman or cURL:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/processor/upload/ \
-F 'source_file=@path/to/source_file.csv' \
-F 'target_file=@path/to/target_file.csv'
```

To generate a report:

```bash
curl -X GET 'http://127.0.0.1:8000/api/v1/processor/report/?report_type=json'

curl -X GET 'http://127.0.0.1:8000/api/v1/processor/report/?report_type=html'

curl -X GET 'http://127.0.0.1:8000/api/v1/processor/report/?report_type=csv'

```
