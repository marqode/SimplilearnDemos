import json
import boto3

s3 = boto3.client("s3")

def fetch_order_from_s3(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return json.loads(response["Body"].read())

def calculate_order_total(order):
    return sum(item["price"] * item["quantity"] for item in order["items"])

def process_orders(event):
    results = []

    for record in event.get("records", []):
        try:
            order_id = record["order_id"]
            order = fetch_order_from_s3(record["bucket"], record["key"])
            total = calculate_order_total(order)
            status = "FLAGGED" if total > 1000 else "OK"

            results.append({
                "order_id": order_id,
                "status": status,
                "total": total
            })

        except Exception as e:
            print(f"Error processing order {record.get('order_id', 'unknown')}: {e}")

    return results