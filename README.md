# Asynchronous Image Processing Backend - image-api

This is a Python-based backend service that allows users to upload one or more images, apply filters (e.g., blur, sharpen, grayscale) and retrieve the processed results asynchronously. Built with FastAPI, Celery, and Redis, it supports scalable image processing and batch downloads.

---

## Features

- Upload multiple images via POST
- Apply filters like Blur, Sharpen, Grayscale, Edges, Smooth
- Asynchronous processing using Celery
- Track job status and readiness
- Download processed images as a ZIP archive
- Auto-generated Swagger UI for API testing

---

## Tech Stack

| Component        | Technology                           |
|------------------|--------------------------------------|
| Frontend         | Swagger UI (via FastAPI)             |
| Backend          | Python (FastAPI + Celery)            |
| Task Queue       | Redis                                |
| Image Processing | Pillow                               |
| Version Control  | Git + GitHub                         |
| Deployment       | Docker                               |

---

## Setup Instructions (Docker Compose)

### 1. Clone the repository

git clone https://github.com/Anubrata12/image-api.git
cd image-api

### 2. Build and start all services

docker-compose up --build

### 3. Access the API
Swagger UI: http://localhost:8000/docs

Upload images via /process-job

Poll status via /status-job/{job_id}

Download results via /download/{job_id}

### 4. Stopping the services

docker-compose down

---

API Endpoints
POST /process-batch: Upload images and apply filter

GET /status-job/{job_id}: Check processing status

GET /download/{job_id}: Download ZIP of processed images

GET /images/{job_id}/{filename}: Access individual images

---

Application Flow
Upload images via /process-batch with a selected filter

Celery tasks apply filters asynchronously

Use /status-batch/{batch_id} to check readiness

Download results via /download/{batch_id}

---

Folder Structure

image-api/
├── main.py              # FastAPI app
├── tasks.py             # Celery image processing
├── processed-images/    # Output folder
├── requirements.txt
└── docker-compose.yml   # Redis + worker setup

Author
Built by Anubrata Dutta Senior Software Engineer | Backend & Cloud Infrastructure


