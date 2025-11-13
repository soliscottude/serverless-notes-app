# 📝 Serverless Notes App

This is a personal portfolio project to learn and practice **serverless architecture on AWS**.

Planned stack:
- AWS Lambda (Python)
- Amazon DynamoDB
- API Gateway (later)
- Simple frontend (later)

---

## ✅ Current backend status

- [x] DynamoDB table `notes` created  
  - Partition key: `noteId` (String)
- [x] IAM role `serverless-notes-lambda-role`  
  - Can write/read DynamoDB and write CloudWatch logs
- [x] Lambda function `serverless-notes-api`  
  - Action `"create"`: write a note into DynamoDB  
  - Action `"list"`: read all notes for a given `userId`
- [ ] API Gateway HTTP endpoints
- [ ] Frontend (web UI)
- [ ] Auth / per-user security

---

## 🧪 Example test events (from Lambda console)

### Create a note

```json
{
  "action": "create",
  "body": {
    "userId": "scott",
    "title": "My first note",
    "content": "Hello from Lambda & DynamoDB!"
  }
}
```

### List notes for one user

```
{
  "action": "list",
  "body": {
    "userId": "scott"
  }
}
```


### 📂 Code structure (so far)
```
serverless-notes-app/
  ├── lambda/
  │   └── notes_handler.py   # Lambda code (create + list notes)
  └── README.md
```
I am building this project step by step and will use it as a real portfolio piece.