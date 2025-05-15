import os
from datetime import datetime, timedelta
from typing import Any

from google.auth import default
from google.cloud import logging_v2
from googleapiclient.discovery import build


def list_cloud_run_jobs(project_number: str) -> list[str]:
    """
    List all cloud run jobs

    Args:
        project_number (str): GCP project number
    
    Returns:
        list[str]: List of cloud run job names 
    """
    credentials, _ = default()

    service = build('run', 'v2', credentials=credentials)

    parent = f"projects/{project_number}/locations/{os.environ['GCP_REGION']}"

    request = service.projects().locations().jobs().list(parent=parent)
    response = request.execute()

    jobs = [i["name"].split("/")[-1] for i in response.get('jobs', [])]
    return jobs


def get_job_executions(project_number: str, job_name: str) -> list[dict[str, Any]]:
    """
    Get latest 20 executions for a cloud run jobs sorted by start time in descending order
    
    Args:
        project_number (str): GCP project number
        job_name (str): Cloud run job name
    
    Returns:
        list[dict[str, Any]]: List of objects with cloud run job status, start time and end time 
    """
    credentials, _ = default()
    service = build('run', 'v2', credentials=credentials)

    parent = f"projects/{project_number}/locations/{os.environ['GCP_REGION']}/jobs/{job_name}"
    request = service.projects().locations().jobs().executions().list(parent=parent)

    response = request.execute()
    executions = response.get('executions', [])

    result = []
    for execution in executions:
        conditions = sorted(execution["conditions"], key=lambda x: datetime.fromisoformat(x["lastTransitionTime"]),
                            reverse=True)
        if conditions:
            result.append(
                {"start_time": datetime.fromisoformat(execution["startTime"]) if execution.get("startTime") else "N/A",
                 "end_time": datetime.fromisoformat(execution["endTime"]) if execution.get("endTime") else "N/A",
                 "type": conditions[0]["type"],
                 "uid": execution["uid"],
                 "execution_id": execution["name"].split("/")[-1],
                 "status": "success" if conditions[0]["state"] == "CONDITION_SUCCEEDED" else "fail"})

    return result


def get_cloud_run_job_execution_logs(project_number: str, job_name: str, execution_id: str):
    """
    Get logs for a specific Cloud Run job execution.

    Args:
        project_number (str): GCP project number.
        job_name (str): Cloud Run job name.
        execution_id (str): Execution ID.

    Returns:
        list[dict]: List of log entries.
    """
    credentials, _ = default()
    client = logging_v2.Client(project=project_number, credentials=credentials)

    now = datetime.now()
    start_time = (now - timedelta(days=30)).isoformat() + "Z"
    end_time = now.isoformat() + "Z"

    log_filter = f'''
    timestamp >= "{start_time}"
    timestamp <= "{end_time}"
    resource.type="cloud_run_job"
    resource.labels.project_id="rl-warehouse"
    resource.labels.location="{os.environ['GCP_REGION']}"
    resource.labels.job_name="{job_name}"
    labels."run.googleapis.com/execution_name"="{execution_id}"
    '''

    entries = client.list_entries(
        filter_=log_filter,
        page_size=200
    )

    logs = []
    for entry in entries:
        message = entry.payload if isinstance(entry.payload, str) else str(entry.payload)
        logs.append({
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else "unknown",
            "severity": entry.severity,
            "message": message
        })

    return logs
