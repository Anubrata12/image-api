from app.tasks import process_image_task, celery_app
from celery.result import AsyncResult
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import uuid
import os
import zipfile


app = FastAPI()
app.mount("/images", StaticFiles(directory="processed-images"), name="images")
job_tasks = {}  # job_id → list of task_ids


@app.post("/process-job")
async def process_job(files: List[UploadFile] = File(...), filter: str = "blur"):
    job_id = str(uuid.uuid4())
    task_ids = []

    for file in files:
        image_bytes = await file.read()
        task = process_image_task.delay(image_bytes, filter, job_id)
        task_ids.append(task.id)

    job_tasks[job_id] = task_ids
    return {"job_id": job_id, "task_ids": task_ids}


@app.get("/status-job/{job_id}")
def get_job_status(job_id: str):
    statuses, all_ready, message = check_job_status(job_id)
    if statuses is None:
        return {"status": "error", "message": message}

    return {
        "job_id": job_id,
        "all_ready": all_ready,
        "all_successful": all_ready,
        "results": statuses
    }


@app.get("/download/{job_id}")
def download_job(job_id: str):
    statuses, all_ready, message = check_job_status(job_id)
    if statuses is None:
        return {"status": "error", "message": message}
    if not all_ready:
        return {"status": "pending", "message": message}

    folder_path = os.path.join("processed-images", job_id)
    zip_path = f"{folder_path}.zip"

    if not os.path.exists(folder_path):
        return {"status": "error", "message": "Processed folder not found"}

    image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
    if not image_files:
        return {"status": "error", "message": "No images found in job folder"}

    if not os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filename in image_files:
                file_path = os.path.join(folder_path, filename)
                zipf.write(file_path, arcname=filename)

    return FileResponse(zip_path, media_type="application/zip", filename=f"{job_id}.zip")


def check_job_status(job_id: str):
    task_ids = job_tasks.get(job_id)
    if not task_ids:
        return None, False, "job not found"

    statuses = []
    all_ready = True

    for task_id in task_ids:
        result = AsyncResult(task_id, app=celery_app)
        ready = result.ready()
        successful = result.successful()

        if not ready or not successful:
            all_ready = False

        status = {
            "task_id": task_id,
            "status": result.status,
            "ready": ready,
            "successful": successful
        }
        if ready and successful:
            status["image_url"] = f"/images/{result.result}"
        statuses.append(status)

    return statuses, all_ready, "Ready" if all_ready else "Images not ready"
