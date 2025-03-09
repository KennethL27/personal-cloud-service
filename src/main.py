from fastapi import FastAPI
from .api import health_check

app = FastAPI(title = "Personal Cloud Service")
app.include_router(health_check.router)

@app.get('/')
async def root():
    return {"message": "Hello World"}