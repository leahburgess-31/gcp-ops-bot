# gcp-ops-bot

A Python-based monitoring utility for **Google Cloud Platform (GCP)** resources. This bot leverages Application Default Credentials (ADC) and various GCP APIs to inspect service accounts, compute instances (VMs), monitoring metrics, and logs.

---

## Features

- **List Custom Service Accounts**  
  Identify non-default (custom) service accounts in a GCP project.

- **Inspect Virtual Machines**  
  List VMs in a specified zone and describe them via self-links.

- **Fetch Monitoring Metrics**  
  Query Cloud Monitoring for recent metrics (CPU, memory, etc.).

- **Retrieve GCP Logs**  
  Get logs from Cloud Logging for specified resources and timeframes.

- **Google GenAI Integration** *(Optional)*  
  Use Google GenAI to interpret logs and metrics (if enabled).

---

## Requirements

Create a virtual environment and activate it:

On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

On Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Authentication

This bot uses **Application Default Credentials (ADC)**.

Set up ADC on your machine:

```bash
gcloud auth application-default login
```

Or set the service account key:

```bash
# On Windows
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json

# On Linux/macOS
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

---

## Usage

```bash
python main.py
```

---

## Environment Variables

Create a `.env` file from `.env.example` for keys or tokens your bot needs.

---

## License

This project is open-sourced under the [MIT License](LICENSE.txt).

---

## Contributing

Pull requests and contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.