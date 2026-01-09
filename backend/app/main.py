from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import io
from uuid import uuid4
import aiofiles
import os
from .tasks import process_csv_task
import redis


app = FastAPI()

# Redis connection for storing results
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
UPLOAD_DIR = "app/storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allow CORS for frontend requests (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        task_id = str(uuid4())
        file_path = f"{UPLOAD_DIR}/{task_id}_{file.filename}"
        async with aiofiles.open(file_path, "wb") as out_file:
            contents = await file.read()
            await out_file.write(contents)
        process_csv_task.delay(task_id, file_path)
        redis_client.set(task_id, "processing")
        return {"message": "Task started", "task_id": task_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
