from google.auth import default
from googleapiclient.discovery import build


def list_custom_service_accounts(project_number: str):
    """
    Lists custom-created service accounts in a GCP project, excluding system-managed ones.

    This function uses Application Default Credentials to authenticate and retrieves
    all service accounts in the specified project via the IAM API. It filters out
    default or system-managed service accounts such as:
    - Compute Engine default service accounts
    - App Engine default service accounts
    - Cloud Build service accounts
    - Google-managed service agents

    Args:
        project_number (str): The GCP project number.

    Returns:
        List[str]: A list of email addresses of custom-created service accounts.
    """
    credentials, _ = default()
    service = build("iam", "v1", credentials=credentials)

    name = f"projects/{project_number}"
    accounts = service.projects().serviceAccounts().list(name=name).execute()

    custom_accounts = []
    for sa in accounts.get("accounts", []):
        email = sa["email"]
        if (
                not email.startswith(f"{project_number}@") and
                "gserviceaccount.com" in email and
                "compute" not in email and
                "cloudbuild" not in email and
                "cloudservices" not in email
        ):
            custom_accounts.append(email)

    return custom_accounts
