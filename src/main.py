from fastapi import FastAPI
from .api import health_check, file_upload

app = FastAPI(title = "Personal Cloud Service")
app.include_router(health_check.router)
app.include_router(file_upload.router)

@app.get('/')
async def root():
    return {"message": "Hello World"}