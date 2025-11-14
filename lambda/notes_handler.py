import json
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Attr

# connect DynamoDB
dynamodb = boto3.resource("dynamodb")

# notes table
table = dynamodb.Table("notes")

# event: json from input
def lambda_handler(event, context):
    '''
    Event structure:
    {
      "action": "create",
      "body": {
        "userId": "scott",
        "title": "First note",
        "content": "Hello from Lambda"
      }
    }
    or:
    {
      "action": "list",
      "body": {
        "userId": "scott"
      }
    }
    '''
    # get action/body from event
    '''
    action = "create"
    body = {"userId": "...", "title": "...", "content": "..."}
    '''

    action = event.get("action")
    body = event.get("body", {})

    # If the request body comes as a JSON string (common when using API Gateway),
    # convert it into a Python dictionary. If parsing fails (body isn't valid JSON),
    # fall back to an empty dict to avoid crashing the function.
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = {}

    # if "create", run handle_create
    if action == "create":
        return handle_create(body)

    # if "list", run handle_list
    elif action == "list":
        return handle_list(body)

    # otherwise, return an error message
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unknown action. Use 'create' or 'list'.",
                "receivedAction": action
            })
        }

# get userID, title and content from body
def handle_create(body: dict):
    user_id = body.get("userId")
    title = body.get("title")
    content = body.get("content")

    # if any of them is null, then return message
    if not user_id or not title or not content:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "userId, title and content are required for create"
            })
        }

    # generate a random ID and document the time
    note_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    # make the contents a record
    item = {
        "noteId": note_id,
        "userId": user_id,
        "title": title,
        "content": content,
        "createdAt": created_at,
    }

    # add the record to DynamoDB
    table.put_item(Item=item)

    # return result
    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Note created in DynamoDB",
            "note": item
        })
    }

# get userID from body
def handle_list(body: dict):
    user_id = body.get("userId")

    # no userID, return message
    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "userId is required for list"
            })
        }

    # scan the table and find the records
    response = table.scan(
        FilterExpression=Attr("userId").eq(user_id)
    )

    # get the records under userID
    items = response.get("Items", [])

    # return result
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Found {len(items)} notes for user {user_id}",
            "notes": items
        })
    }
