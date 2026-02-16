import json
import logging
from typing import Dict, List, Any

import boto3

logger = logging.getLogger(__name__)
s3 = boto3.client("s3")

FLAG_THRESHOLD = 1000


def calculate_order_total(items: List[Dict[str, Any]]) -> float:
    """Calculate total price for order items."""
    return sum(item["price"] * item["quantity"] for item in items)


def get_order_from_s3(bucket: str, key: str) -> Dict[str, Any]:
    """Retrieve and parse order data from S3."""
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read().decode("utf-8")
    return json.loads(body)


def process_single_order(record: Dict[str, str]) -> Dict[str, Any]:
    """Process a single order record."""
    order_id = record["order_id"]
    order = get_order_from_s3(record["bucket"], record["key"])
    total = calculate_order_total(order["items"])
    
    return {
        "order_id": order_id,
        "status": "FLAGGED" if total > FLAG_THRESHOLD else "OK",
        "total": total
    }


def process_orders(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process multiple order records from event."""
    results = []
    
    for record in event.get("records", []):
        try:
            result = process_single_order(record)
            results.append(result)
        except Exception as e:
            logger.error(f"Error processing order {record.get('order_id', 'unknown')}: {e}")
    
    return results
