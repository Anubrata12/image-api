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
```bash
git clone https://github.com/Anubrata12/image-api.git
cd image-api
```
### 2. Build and start all services
```bash
docker-compose up --build
```
### 3. Access the API

Swagger UI: http://localhost:8000/docs

Upload images via /process-job

Poll status via /status-job/{job_id}

Download results via /download/{job_id}

### 4. Stopping the services
```bash
docker-compose down
```
---

## API Endpoints

POST /process-batch: Upload images and apply filter

GET /status-job/{job_id}: Check processing status

GET /download/{job_id}: Download ZIP of processed images

GET /images/{job_id}/{filename}: Access individual images

---

## Application Flow

### This backend processes images asynchronously using FastAPI, Celery, Redis, and Pillow. Here's how it works:

#### 1. User uploads images via /process-batch

- FastAPI receives the request with multiple image files and a selected filter.

- A unique batch_id is generated.

- For each image, FastAPI dispatches a Celery task using Redis as the broker.

#### 2. Redis queues the tasks

- Redis stores the task metadata and routes them to available Celery workers.

#### 3. Celery workers process images

- Each worker retrieves the image bytes and applies the requested filter using Pillow.

-  Processed images are saved to processed-images/{batch_id}/.

#### 4. User polls /status-batch/{batch_id}

-  FastAPI checks task status via Redis using AsyncResult.

-  If all tasks are complete, image URLs are returned.

#### 5. User downloads results via /download/{batch_id}

- FastAPI bundles all processed images into a ZIP archive.

- The archive is returned as a downloadable file.

---

Author
Built by Anubrata Dutta Senior Software Engineer | Backend & Cloud Infrastructure


