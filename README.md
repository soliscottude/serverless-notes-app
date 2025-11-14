# 📝 Serverless Notes App

A complete, production-style **serverless notes application** built on AWS, featuring:

- AWS Lambda (Python) backend  
- API Gateway (HTTP API) routing  
- DynamoDB for persistent NoSQL storage  
- A modern static frontend (HTML/CSS/JavaScript)  
- Global hosting using S3 + CloudFront  
- Automatic deployment using GitHub Actions  

This project demonstrates a real-world serverless architecture from end to end, from frontend → API → compute → database → CI/CD → global CDN delivery.

---

## 🚀 Live Demo

Frontend (CloudFront):

https://dipmx1tgj1dm8.cloudfront.net/

This is the deployed version of the application using S3 and CloudFront.

---

## 📘 Overview

This is a clean, single-page notes application powered entirely by serverless AWS services.  

Users can:

- Create notes  
- View notes by user  
- Interact with a real backend API  
- Use a fully deployed global frontend  

The backend is built using **AWS Lambda + DynamoDB**, exposed through **API Gateway**, while the frontend is hosted on **S3** and distributed worldwide through **CloudFront** for high performance.

All frontend updates are automatically deployed using **GitHub Actions**, providing a complete CI/CD workflow.

This project demonstrates practical cloud engineering skills, including serverless API design, infrastructure configuration, static hosting, IAM permissions, CI/CD automation, and scalable architecture patterns.

---

## 🧠 Features

- Create notes (action: "create")

- List notes per user (action: "list")

- DynamoDB for persistent storage

- Lambda (Python) for backend business logic

- HTTP API (API Gateway v2) as the API entry point

- HTML/CSS/JavaScript frontend

- Fully deployed using S3 + CloudFront

- CORS-enabled for browser access

---

## 🧱 Tech Stack

#### Backend:

- AWS Lambda (Python 3.x)

- API Gateway (HTTP API v2)

- DynamoDB

- IAM (least privilege)

#### Frontend:

- HTML

- CSS

- Vanilla JavaScript

#### Hosting:

Amazon S3

Amazon CloudFront (CDN)

---

## 🗂 Project Structure
```
serverless-notes-app/
│
├── lambda/
│   └── notes_handler.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .github/
│   └── workflows/
│       └── deploy-frontend.yml
│
├── README.md
└── screenshots/
```

---

## 🧩 Architecture

```
Browser (CloudFront URL)
         │
         ▼
CloudFront (CDN)
         │
         ▼
S3 Static Website Hosting
         │
         ▼
Frontend JS fetches →
API Gateway (HTTP API)
         │
         ▼
AWS Lambda (Python)
         │
         ▼
DynamoDB (notes table)
```

---

## 📦 DynamoDB Schema

#### Table name: notes

#### Fields (all strings):

- noteId — UUID (primary key)

- userId — owner of the note

- title — note title

- content — note body

- createdAt — ISO timestamp

---

## 🔌 Lambda API (Action-Based Routing)

The application uses one HTTP endpoint:

```
POST /notes
```

and determines the operation based on the "action" field.

#### Create a note

```json
{
  "action": "create",
  "body": {
    "userId": "scott",
    "title": "My first note",
    "content": "Created via Lambda + DynamoDB"
  }
}
```

#### List notes

```json
{
  "action": "list",
  "body": {
    "userId": "scott"
  }
}
```

---

## 🖥 Local Frontend Usage

To run the frontend locally:

```
cd frontend
python3 -m http.server 8000
```

Then open:
```
http://localhost:8000
```

The API URL is written directly inside app.js.

---

## 🌐 Deployment (S3 + CloudFront)

This project is deployed using AWS S3 + CloudFront for global distribution.

#### 1. S3 Hosting

- Created a dedicated bucket

- Enabled Static Website Hosting

- Uploaded index.html, style.css, app.js

- Added public-read bucket policy for GET access

- Verified the website endpoint works

#### 2. CloudFront Configuration

- Origin: S3 website endpoint

- Viewer Protocol Policy: Redirect HTTP → HTTPS

- Default Root Object: index.html

- Distribution name: serverless-notes-frontend

- Output URL:
https://dipmx1tgj1dm8.cloudfront.net/

This forms a production-grade serverless deployment.

---

## ⚙️ CI/CD – Automatic Frontend Deployment

The frontend is automatically deployed using **GitHub Actions** whenever changes are pushed to the repository.

### Workflow

File: `.github/workflows/deploy-frontend.yml`

The workflow:

- Checks out the repository
- Configures AWS credentials from GitHub Secrets
- Syncs the `frontend/` folder to the S3 bucket
- Invalidates the CloudFront cache so the latest version is served

High-level steps:

1. **AWS IAM user for CI/CD**
   - Created a dedicated IAM user with permissions for:
     - `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket` on the frontend S3 bucket
     - `cloudfront:CreateInvalidation` on the CloudFront distribution
   - Stored its keys as GitHub Secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

2. **GitHub Actions workflow**
   - Uses `aws-actions/configure-aws-credentials` to authenticate to AWS
   - Runs `aws s3 sync frontend/ s3://<my-bucket> --delete` to deploy updated files
   - Runs `aws cloudfront create-invalidation --distribution-id <my-distribution-id> --paths "/*"` to refresh the CDN

3. **Trigger**
   - The workflow is triggered on pushes to the `main` branch (and can be manually triggered via `workflow_dispatch`).

This CI/CD setup means that updating the frontend is as simple as:

- `git commit`  
- `git push`  

The website on CloudFront is automatically updated with the latest version.

---

## 🧠 What I Learned

- Designing a full serverless backend with Lambda

- DynamoDB schema design and querying

- API Gateway (HTTP API) configuration and CORS

- Frontend → API integration

- Hosting static websites on S3

- Distributing globally with CloudFront

- IAM role permissions for Lambda

- Deploying a complete cloud application end-to-end

---

## 👨🏻‍💻 Author

Scott Yang

Cloud Support / DevOps Learner

Auckland, New Zealand

GitHub: https://github.com/soliscottude