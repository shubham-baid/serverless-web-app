import os
import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'StudentRecords'))

def _json(obj):
    """Safe JSON: converts Decimal to str."""
    return json.dumps(obj, default=lambda o: str(o))

def _resp(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            # CORS (adjust origin if you have a specific frontend)
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": _json(body)
    }

def lambda_handler(event, context):
    method = event.get("httpMethod", "")
    # Preflight for browsers
    if method == "OPTIONS":
        return _resp(200, {"ok": True})

    body = event.get("body")
    if isinstance(body, str) and body:
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return _resp(400, {"error": "Invalid JSON body"})
    elif body is None:
        body = {}

    qs = event.get("queryStringParameters") or {}
    student_id = (
        body.get("student_id")
        or qs.get("student_id")
        or (event.get("pathParameters") or {}).get("student_id")
    )

    try:
        if method == "POST":
            # Create (fail if already exists)
            if not student_id:
                return _resp(400, {"error": "student_id is required"})
            # Use condition to avoid accidental overwrite
            item = body
            # Ensure student_id in item
            item["student_id"] = student_id
            table.put_item(
                Item=item,
                ConditionExpression=Attr("student_id").not_exists()
            )
            return _resp(201, {"message": "Created", "student": item})

        elif method == "GET":
            # Read by student_id
            if not student_id:
                return _resp(400, {"error": "student_id is required"})
            res = table.get_item(Key={"student_id": student_id})
            item = res.get("Item")
            if not item:
                return _resp(404, {"error": "Not found"})
            return _resp(200, item)

        elif method == "PUT":
            # Update: accept arbitrary attributes except student_id
            if not student_id:
                return _resp(400, {"error": "student_id is required"})
            updates = {k: v for k, v in body.items() if k != "student_id"}
            if not updates:
                return _resp(400, {"error": "No fields to update"})
            # Build dynamic UpdateExpression
            expr_parts = []
            expr_attr_names = {}
            expr_attr_values = {}
            for i, (k, v) in enumerate(updates.items(), start=1):
                name_key = f"#f{i}"
                value_key = f":v{i}"
                expr_parts.append(f"{name_key} = {value_key}")
                expr_attr_names[name_key] = k
                expr_attr_values[value_key] = v

            res = table.update_item(
                Key={"student_id": student_id},
                UpdateExpression="SET " + ", ".join(expr_parts),
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ConditionExpression=Attr("student_id").exists(),
                ReturnValues="ALL_NEW"
            )
            return _resp(200, {"message": "Updated", "student": res["Attributes"]})

        elif method == "DELETE":
            if not student_id:
                return _resp(400, {"error": "student_id is required"})
            table.delete_item(
                Key={"student_id": student_id},
                ConditionExpression=Attr("student_id").exists()
            )
            return _resp(200, {"message": "Deleted", "student_id": student_id})

        else:
            return _resp(405, {"error": f"Method {method} not allowed"})

    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("ConditionalCheckFailedException",):
            # Create when exists, Update/Delete when missing
            return _resp(409, {"error": "Condition failed (exists/missing conflict)"})
        return _resp(500, {"error": "DynamoDB error", "detail": str(e)})
    except Exception as e:
        return _resp(500, {"error": "Unhandled error", "detail": str(e)})
