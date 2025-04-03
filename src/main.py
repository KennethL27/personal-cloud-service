from fastapi import FastAPI
from pathlib import Path
import pkgutil
import importlib

app = FastAPI(title = "Personal Cloud Service")

def include_routers():
    package = "src.api"
    api_path = Path(__file__).parent / "api"

    for module_info in pkgutil.walk_packages([str(api_path)], prefix=f"{package}."):
        module = importlib.import_module(module_info.name)
        
        if hasattr(module, "router"):
            # Convert module path to URL prefix (e.g., "app.api.file.upload" -> "/file/upload")
            relative_path = module_info.name.replace(package + ".", "").replace(".", "/")
            prefix = f"/{relative_path}"

            app.include_router(module.router, prefix=prefix)
            
include_routers()

@app.get('/')
async def root():
    return {"message": "Hello World"}