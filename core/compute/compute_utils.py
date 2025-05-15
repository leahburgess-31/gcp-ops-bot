import re
from datetime import datetime, timedelta

from google.auth import default
from google.cloud import monitoring_v3
from googleapiclient import discovery


def list_vms(project_number: str, zone_name: str) -> list[dict]:
    """
    List VMs across all zones.
    
    Args:
        project_number (str): GCP project number
        zone_name (str): Zone to check for VMs
    
    Returns:
        list[dict]: A list of VMs in the requested zone and project. Each VM is represented as a dictionary.
    """
    credentials, _ = default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    result = service.instances().list(project=project_number, zone=zone_name).execute()
    return result.get('items', [])


def describe_vm(self_link: str) -> dict:
    """
    Get full metadata of a VM
    
    Args:
        self_link (str): Self link of a VM
    
    Returns:
        dict: Information about the requested VM

    Raises:
        ValueError: If self link is invalid
    """
    match = re.match(
        r"https://www.googleapis.com/compute/v1/projects/([^/]+)/zones/([^/]+)/instances/([^/]+)",
        self_link
    )
    if not match:
        raise ValueError("Invalid VM selfLink format")

    project, zone, instance_name = match.groups()

    credentials, _ = default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    request = service.instances().get(project=project, zone=zone, instance=instance_name)
    response = request.execute()
    return response


def monitor_vm(self_link: str) -> dict[str, dict[str, list]]:
    """
    Get CPU utilization for last 5 minutes for requested VM

    Args:
        self_link (str): VM self link

    Returns:
        dict[str, dict[str, list]]: Mapping of instance name to an object with end_time and value arrays
    """
    match = re.match(
        r"https://www.googleapis.com/compute/v1/projects/([^/]+)/zones/([^/]+)/instances/([^/]+)",
        self_link
    )
    if not match:
        raise ValueError("Invalid VM selfLink format")

    project_id, zone, instance_name = match.groups()

    credentials, _ = default()
    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    project_name = f"projects/{project_id}"

    now = datetime.now()
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(now.timestamp())},
        start_time={"seconds": int((now - timedelta(minutes=5)).timestamp())},
    )

    instance_filter = (
        f'metric.type="compute.googleapis.com/instance/cpu/utilization" '
        f'AND metric.labels.instance_name="{instance_name}"'
    )

    request = {
        "name": project_name,
        "filter": instance_filter,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    }

    page_result = client.list_time_series(
        request=request
    )

    metric_data = {}
    for result in page_result:
        instance_name = result.metric.labels["instance_name"]
        metric_data[instance_name] = {"end_time": [], "value": []}
        for point in result.points:
            metric_data[instance_name]["end_time"].append(point.interval.end_time)
            metric_data[instance_name]["value"].append(point.value.double_value)
    return metric_data
