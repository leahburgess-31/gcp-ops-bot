# gcp-ops-bot

`gcp-ops-bot` is a Python-based monitoring utility for Google Cloud Platform (GCP) resources. It leverages Application Default Credentials (ADC) and various GCP APIs to inspect service accounts, compute instances (VMs), monitoring metrics, and logs.

Optionally, it integrates with **Google GenAI** to provide natural-language insights and interpretations of logs and metrics.

---

## 🔍 Features

- **List Custom Service Accounts** — Identify non-default service accounts in a GCP project.

- **Inspect Virtual Machines** — List and describe VMs in a given zone.

- **Fetch Monitoring Metrics** — Query recent CPU, memory, and performance metrics.

- **Retrieve GCP Logs** — Pull logs from Cloud Logging for specific resources and timeframes.

- **GenAI Integration (Optional)** — Use Google GenAI to interpret logs and metrics in plain English.

---

## 🚀 Quick Start

Run the bot:

```bash
python main.py
```

You’ll see:

```
GCP Monitoring Bot started. Type 'q', 'quit', or 'exit' to stop.
--------------------------------------------------
User :>
```

Then type natural-language prompts like:

```
List all VMs in us-central1-a
```

---

## 📚 Full Documentation

Visit the [Wiki](https://github.com/Retailogists/gcp-ops-bot/wiki) for detailed guides:

- [Installation & Setup](https://github.com/Retailogists/gcp-ops-bot/wiki/Installation-&-Setup)
- [Usage Guide with Examples](https://github.com/Retailogists/gcp-ops-bot/wiki/Usage-Guide)
- [Authentication & Permissions](https://github.com/Retailogists/gcp-ops-bot/wiki/Authentication-&-Permissions)

---

## Environment Variables

Create a `.env` file using `.env.example`:

```env
GENAI_API_KEY=your_genai_api_key     # Optional if not using GenAI
GCP_PROJECT_ID=your_project_id
GCP_PROJECT_NUMBER=your_project_number
GCP_REGION=us-central1
GCP_ZONE=us-central1-a
```

---

## 🤝 Contributing

We welcome contributions of all kinds!

- Fork the repo, create a branch, and submit a pull request.
- See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License.
