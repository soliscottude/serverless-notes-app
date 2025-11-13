import json
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("notes")


def lambda_handler(event, context):
    """
    期望的 event 结构：
    {
      "action": "create",
      "body": {
        "userId": "scott",
        "title": "First note",
        "content": "Hello from Lambda"
      }
    }
    或：
    {
      "action": "list",
      "body": {
        "userId": "scott"
      }
    }
    """

    action = event.get("action")
    body = event.get("body", {})

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = {}

    if action == "create":
        return handle_create(body)

    elif action == "list":
        return handle_list(body)

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unknown action. Use 'create' or 'list'.",
                "receivedAction": action
            })
        }


def handle_create(body: dict):
    user_id = body.get("userId")
    title = body.get("title")
    content = body.get("content")

    if not user_id or not title or not content:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "userId, title and content are required for create"
            })
        }

    note_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    item = {
        "noteId": note_id,
        "userId": user_id,
        "title": title,
        "content": content,
        "createdAt": created_at,
    }

    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Note created in DynamoDB",
            "note": item
        })
    }


def handle_list(body: dict):
    user_id = body.get("userId")

    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "userId is required for list"
            })
        }

    response = table.scan(
        FilterExpression=Attr("userId").eq(user_id)
    )

    items = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Found {len(items)} notes for user {user_id}",
            "notes": items
        })
    }
