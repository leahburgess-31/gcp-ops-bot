"""
Simple cost monitoring utilities for GCP projects.

This module provides basic cost tracking functionality using Google Cloud APIs.
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from google.auth import default
from google.cloud import billing_v1




def get_current_month_costs(project_id: str) -> Dict[str, Any]:
    """
    Get current month's total costs for a project
    
    Args:
        project_id (str): GCP project ID
    
    Returns:
        Dict[str, Any]: Current month cost information
    """
    try:
        credentials, _ = default()
        billing_client = billing_v1.CloudBillingClient(credentials=credentials)
        
        # Get billing account info
        project_name_full = f"projects/{project_id}"
        project = billing_client.get_project_billing_info(name=project_name_full)
        
        # Try to get real cost data from BigQuery billing export
        try:
            from google.cloud import bigquery
            bq_client = bigquery.Client(credentials=credentials, project=project_id)
            
            now = datetime.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            query = f"""
            SELECT SUM(cost) as total_cost, currency
            FROM `{project_id}.billing_export.gcp_billing_export_v1_*`
            WHERE _PARTITIONTIME >= TIMESTAMP('{month_start.strftime('%Y-%m-%d')}')
            GROUP BY currency
            """
            
            query_job = bq_client.query(query)
            results = query_job.result()
            
            total_cost = 0.0
            currency = "USD"
            for row in results:
                total_cost = float(row.total_cost) if row.total_cost else 0.0
                currency = row.currency if row.currency else "USD"
                break
            
            return {
                "total_cost": total_cost,
                "currency": currency,
                "billing_account": project.billing_account_name
            }
            
        except Exception:
            # If BigQuery fails, return basic billing info
            return {
                "total_cost": 0.0,
                "currency": "USD",
                "billing_account": project.billing_account_name,
                "note": "Enable billing export for cost data"
            }
        
    except Exception as e:
        return {"error": f"Could not access billing: {str(e)}"}


def get_cost_by_service(project_id: str, days: int = 30) -> List[Dict[str, Any]]:
    """
    Get costs broken down by GCP service
    
    Args:
        project_id (str): GCP project ID
        days (int): Number of days to look back
    
    Returns:
        List[Dict[str, Any]]: Cost breakdown by service
    """
    try:
        credentials, _ = default()
        from google.cloud import bigquery
        
        bq_client = bigquery.Client(credentials=credentials, project=project_id)
        
        # Simple query for service costs
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = f"""
        SELECT 
            service.description as service_name,
            SUM(cost) as total_cost
        FROM `{project_id}.billing_export.gcp_billing_export_v1_*`
        WHERE _PARTITIONTIME >= TIMESTAMP('{start_date.strftime('%Y-%m-%d')}')
        GROUP BY service_name
        ORDER BY total_cost DESC
        """
        
        query_job = bq_client.query(query)
        results = query_job.result()
        
        service_costs = []
        for row in results:
            service_costs.append({
                "service": row.service_name,
                "cost": round(float(row.total_cost), 2) if row.total_cost else 0.0
            })
        
        return service_costs
        
    except Exception as e:
        return [{"service": "Error", "cost": 0.0, "error": str(e)}]


def get_cost_trends(project_id: str, days: int = 30) -> List[Dict[str, Any]]:
    """
    Get daily cost trends for the specified period
    
    Args:
        project_id (str): GCP project ID
        days (int): Number of days to analyze
    
    Returns:
        List[Dict[str, Any]]: Daily cost data
    """
    try:
        credentials, _ = default()
        from google.cloud import bigquery
        
        bq_client = bigquery.Client(credentials=credentials, project=project_id)
        
        # Simple query for daily costs
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = f"""
        SELECT 
            DATE(usage_start_time) as usage_date,
            SUM(cost) as daily_cost
        FROM `{project_id}.billing_export.gcp_billing_export_v1_*`
        WHERE _PARTITIONTIME >= TIMESTAMP('{start_date.strftime('%Y-%m-%d')}')
        GROUP BY usage_date
        ORDER BY usage_date
        """
        
        query_job = bq_client.query(query)
        results = query_job.result()
        
        trends = []
        for row in results:
            trends.append({
                "date": row.usage_date.strftime("%Y-%m-%d"),
                "cost": round(float(row.daily_cost), 2) if row.daily_cost else 0.0
            })
        
        return trends
        
    except Exception as e:
        return [{"date": datetime.now().strftime("%Y-%m-%d"), "cost": 0.0, "error": str(e)}]




def get_resource_costs(project_id: str, resource_type: str = "all") -> List[Dict[str, Any]]:
    """
    Get cost breakdown by specific resource types
    
    Args:
        project_id (str): GCP project ID
        resource_type (str): Type of resource to analyze
    
    Returns:
        List[Dict[str, Any]]: Resource cost breakdown
    """
    try:
        credentials, _ = default()
        from google.cloud import bigquery
        
        bq_client = bigquery.Client(credentials=credentials, project=project_id)
        
        # Simple query for resource costs
        query = f"""
        SELECT 
            sku.description as resource_type,
            SUM(cost) as total_cost
        FROM `{project_id}.billing_export.gcp_billing_export_v1_*`
        WHERE _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        GROUP BY resource_type
        ORDER BY total_cost DESC
        LIMIT 10
        """
        
        query_job = bq_client.query(query)
        results = query_job.result()
        
        resource_costs = []
        for row in results:
            resource_costs.append({
                "resource_type": row.resource_type,
                "cost": round(float(row.total_cost), 2) if row.total_cost else 0.0
            })
        
        return resource_costs
        
    except Exception as e:
        return [{"resource_type": "Error", "cost": 0.0, "error": str(e)}]

