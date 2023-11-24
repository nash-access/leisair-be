# routers/detection.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from ..celery_worker import process_file

router = APIRouter()

class DetectionRequest(BaseModel):
    file_path: str

@router.post("/detect")
async def detect_file(request: DetectionRequest):
    print("Received request to detect file: ", request.file_path)
    process_file.delay(request.file_path)  # Enqueue the task to Celery
    return {"message": "Detection started"}

# @router.post("/detect")
# async def detect_file(request: DetectionRequest, background_tasks: BackgroundTasks):
#     print("Received request to detect file: ", request.file_path)
#     background_tasks.add_task(process_file, request.file_path)
#     return {"message": "Detection started"}

# def process_file(file_path):
#     print("Starting detection on file: ", file_path)
#     # Implement detection logic here
#     pass  
