from celery import Celery
from PIL import Image, ImageFilter, ImageOps
import io
import os
import uuid
import time

# Configure Celery with Redis as broker and backend
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_image_task(image_bytes, filter, job_id=None):

    time.sleep(60)
    image = Image.open(io.BytesIO(image_bytes))

    # Apply filter using dispatch map
    filter_map = {
        "blur": lambda img: img.filter(ImageFilter.BLUR),
        "sharpen": lambda img: img.filter(ImageFilter.SHARPEN),
        "grayscale": lambda img: ImageOps.grayscale(img),
        "edges": lambda img: img.filter(ImageFilter.FIND_EDGES),
        "smooth": lambda img: img.filter(ImageFilter.SMOOTH)
    }

    if filter not in filter_map:
        raise ValueError(f"Unsupported filter: {filter}")

    image = filter_map[filter](image)

    folder = "processed-images"
    if job_id:
        folder = f"{folder}/{job_id}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{uuid.uuid4()}.jpg"
    output_path = f"{folder}/{filename}"
    image.save(output_path)
    return filename if not job_id else f"{job_id}/{filename}"

