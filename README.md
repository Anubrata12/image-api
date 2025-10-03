# Asynchronous Image Processing Backend - image-api

This is a Python-based backend service that allows users to upload one or more images, apply filters (e.g., blur, sharpen, grayscale) and retrieve the processed results asynchronously. Built with FastAPI, Celery, and Redis, it supports scalable image processing and batch downloads.

---

## Features

- Upload multiple images via POST
- Apply filters like Blur, Sharpen, Grayscale, Edges, Smooth
- Asynchronous processing using Celery
- Track job status
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

POST /process-job: Upload images and apply filter

GET /status-job/{job_id}: Check processing status

GET /download/{job_id}: Download ZIP of processed images

GET /images/{job_id}/{filename}: Access individual images

---

## Application Flow

### This app processes images asynchronously using FastAPI, Celery, Redis, and Pillow

#### 1. User uploads images via /process-job

- FastAPI receives request with multiple images and a filter.

- Unique job_id is generated.

- For each image, FastAPI dispatches a Celery task using Redis as broker.

#### 2. Redis queues the tasks

- Redis stores the task metadata and routes them to available Celery workers.

#### 3. Celery workers process images

- Each worker retrieves image bytes and applies the requested filter using Pillow.

- Processed images are saved to processed-images/{job_id}/ folder.

#### 4. User polls /status-job/{job_id}

- FastAPI checks task status via Redis using AsyncResult.

- If all tasks are complete, image URLs are returned.

#### 5. User downloads results via /download/{job_id}

- FastAPI bundles all processed images into a ZIP archive.

- The archive is returned as a downloadable file.

---

## Assumptions in the Project

#### 1. Asynchronous Processing is Required
Image operations are not performed inline during the POST request.

Tasks are dispatched to a background worker (Celery) for non-blocking execution.

#### 2. Multiple Images Can Be Uploaded
The API must support batch uploads via a single POST request.

Each image is processed independently but tracked under a shared job_id.

#### 3. Filter Selection is User-Driven
The user specifies a filter (e.g., blur, sharpen) during upload.

The backend must support multiple filter types, extensible.

#### 4. Job Status Must Be Trackable
Each upload triggers one or more background tasks.

The system must expose a status-check endpoint to query readiness or progress.

#### 5. Processed Output Must Be Downloadable
Once all tasks are complete, the user can download the results.

Output is bundled (e.g., ZIP archive) and served via a dedicated endpoint.

#### 6. Image Processing is Local
Filters are applied using a local library (e.g., Pillow).

No external APIs or cloud services are assumed for image manipulation.

#### 7. Temporary Storage is Acceptable
Processed images are saved to disk (e.g., processed-images/) under a job-specific folder.

Long-term persistence or CDN hosting is not required.

#### 8. No Authentication or User Accounts
The system is assumed to be anonymous — no login, user tracking, or access control.

job_id is the only identifier used for retrieval.

#### 9. Stateless API Design
FastAPI endpoints are stateless; job tracking is done via Redis and in-memory mappings.

No database is assumed for job metadata or user history.

#### 10. Dockerized Local Deployment
The system is expected to run via Docker Compose, orchestrating FastAPI, Redis, and Celery.

No assumptions about cloud deployment or Kubernetes.

---

Author
Built by Anubrata Dutta | Senior Software Engineer | Backend & Cloud Infrastructure


