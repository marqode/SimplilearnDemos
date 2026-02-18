import json
import boto3

s3 = boto3.client("s3")

def process_orders(event):
    results = []
    total = 0

    for record in event.get("records", []):
        try:
            order_id = record["order_id"]
            bucket = record["bucket"]
            key = record["key"]

            response = s3.get_object(Bucket=bucket, Key=key)
            body = response["Body"].read().decode("utf-8")
            order = json.loads(body)

            for item in order["items"]:
                total += item["price"] * item["quantity"]

            if total > 1000:
                results.append({
                    "order_id": order_id,
                    "status": "FLAGGED",
                    "total": total
                })
            else:
                results.append({
                    "order_id": order_id,
                    "status": "OK",
                    "total": total
                })

        except Exception as e:
            print("Error processing order", e)

    return results