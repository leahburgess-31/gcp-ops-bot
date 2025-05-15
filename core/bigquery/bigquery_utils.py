from datetime import datetime, timedelta
from typing import Any

from google.cloud import bigquery


def list_datasets(project_id: str) -> list[str]:
    """
    List all datasets in a project

    Args:
        project_id (str): GCP project ID
    
    Returns:
        list[str]: List of dataset names
    """
    client = bigquery.Client(project=project_id)

    datasets = [dataset.reference.dataset_id for dataset in list(client.list_datasets())]
    return datasets


def get_bigquery_usage_by_user(project_id: str, last_n_days: int) -> list[dict[str, Any]]:
    """
    Get bibytes processed by user email for last n days
    Includes a flag for service account

    Args:
        project_id (str): Project ID
        last_n_days (int): Number of days in past to fetch data from 
    
    Returns:
        list[dict[str, Any]]: List of objects where each object represents a user
    """
    client = bigquery.Client(project=project_id)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=last_n_days)

    query = f"""
        SELECT
            user_email,
            COUNT(*) AS job_count,
            SUM(total_bytes_processed) AS total_bytes_processed
        FROM
            `{project_id}.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
        WHERE
            DATETIME(creation_time, 'America/Toronto') BETWEEN DATETIME('{start_time.isoformat()}') AND DATETIME('{end_time.isoformat()}')
            AND state = 'DONE'
            AND job_type = 'QUERY'
        GROUP BY
            user_email
        ORDER BY
            total_bytes_processed DESC
    """

    query_job = client.query(query)
    results = query_job.result()

    usage_stats = []
    for row in results:
        usage_stats.append({
            "user_email": row["user_email"],
            "is_service_account": row["user_email"].endswith("gserviceaccount.com"),
            "job_count": row["job_count"],
            "total_bytes_processed": row["total_bytes_processed"]
        })

    return usage_stats


def get_bigquery_usage_by_day_user(project_id: str, last_n_days: int) -> list[dict[str, Any]]:
    """
    Get bigquery bytes processed by day by user for last n days

    Args:
        project_id (str): Bigquery project ID
        last_n_days (int): Number of days in past to fetch data from 
    
    Returns:
        list[dict[str, Any]]: List of objects where each object represents a user
    """
    client = bigquery.Client(project=project_id)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=last_n_days)

    query = f"""
        SELECT
            DATETIME(creation_time, 'America/Toronto') AS creation_time,
            user_email,
            COUNT(*) AS job_count,
            SUM(total_bytes_processed) AS total_bytes_processed
        FROM
            `{project_id}.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
        WHERE
            DATETIME(creation_time, 'America/Toronto') BETWEEN DATETIME('{start_time.isoformat()}') AND DATETIME('{end_time.isoformat()}')
            AND state = 'DONE'
            AND job_type = 'QUERY'
        GROUP BY
            DATETIME(creation_time, 'America/Toronto'), user_email
        ORDER BY
            creation_time ASC
    """

    query_job = client.query(query)
    results = query_job.result()

    usage_stats = []
    for row in results:
        usage_stats.append({
            "date": row["creation_time"],
            "user_email": row["user_email"],
            "job_count": row["job_count"],
            "total_bytes_processed": row["total_bytes_processed"]
        })

    return usage_stats


def get_bytes_loaded_to_dataset(project_id: str, dataset_name: str, last_n_days: int) -> list[dict[str, Any]]:
    """
    Get number of bytes loaded into a dataset through load job for last n days, does not include data loaded using CREATE TABLE AS SELECT (CTAS) or INSERT INTO statements.

    Args:
        project_id (str): BigQuery project ID
        dataset_name (str): Dataset to investigate
        last_n_days (int): Number of days in past to fetch data from 
    
    Returns:
        list[dict[str, Any]]: List of objects each object representing bytes loaded by a user on a date
    """
    client = bigquery.Client(project=project_id)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=last_n_days)

    query = f"""
        SELECT
            DATETIME(creation_time, 'America/Toronto') AS creation_time,
            SUM(total_bytes_processed) AS bytes_loaded
        FROM
            `{project_id}.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
        WHERE
            DATETIME(creation_time, 'America/Toronto') BETWEEN DATETIME('{start_time.isoformat()}') AND DATETIME('{end_time.isoformat()}')
            AND state = 'DONE'
            AND job_type = 'LOAD'
            AND destination_table.dataset_id = '{dataset_name}'
        GROUP BY DATETIME(creation_time, 'America/Toronto')
        ORDER BY creation_time ASC
    """

    query_job = client.query(query)
    results = query_job.result()

    data_loaded = []
    for row in results:
        data_loaded.append({
            "date": row["creation_time"],
            "bytes_loaded": row["bytes_loaded"]
        })

    return data_loaded
