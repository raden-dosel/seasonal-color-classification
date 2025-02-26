import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from app.tasks import create_task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    task = create_task.delay(contents)
    return {"task_id": task.id, "message": "pending"}

@app.get("/task-result/{task_id}")
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    if result.ready():
        return JSONResponse(content={"status": result.status, "result": result.result})
    else:
        return JSONResponse(content={"status": result.status})





