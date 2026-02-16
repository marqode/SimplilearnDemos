import json
import boto3
from typing import List, Dict, Any

s3 = boto3.client("s3")

FLAG_THRESHOLD = 1000
STATUS_FLAGGED = "FLAGGED"
STATUS_OK = "OK"

def get_order_from_s3(bucket: str, key: str) -> Dict[str, Any]:
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read().decode("utf-8")
    return json.loads(body)

def calculate_order_total(order: Dict[str, Any]) -> float:
    return sum(item["price"] * item["quantity"] for item in order["items"])

def create_result(order_id: str, total: float) -> Dict[str, Any]:
    status = STATUS_FLAGGED if total > FLAG_THRESHOLD else STATUS_OK
    return {"order_id": order_id, "status": status, "total": total}

def process_single_order(record: Dict[str, str]) -> Dict[str, Any]:
    order_id = record["order_id"]
    bucket = record["bucket"]
    key = record["key"]
    
    order = get_order_from_s3(bucket, key)
    total = calculate_order_total(order)
    return create_result(order_id, total)

def process_orders(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = []
    
    for record in event.get("records", []):
        try:
            result = process_single_order(record)
            results.append(result)
        except Exception as e:
            print(f"Error processing order {record.get('order_id', 'unknown')}: {e}")
    
    return results