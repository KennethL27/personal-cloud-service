from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pkgutil
import importlib
from src.api.auth.dependencies import get_current_user
from dotenv import load_dotenv
from src.database.initializer import DatabaseInitializer

load_dotenv()

app = FastAPI(title = "Personal Cloud Service")
DatabaseInitializer()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Your Next.js dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def include_routers():
    package = "src.api"
    api_path = Path(__file__).parent / "api"

    for module_info in pkgutil.walk_packages([str(api_path)], prefix=f"{package}."):
        module = importlib.import_module(module_info.name)
        
        if hasattr(module, "router"):
            relative_path = convert_module_path_to_url_prefix(module_info, package)
            prefix = f"/{relative_path}"

            if relative_path not in ["auth/login", "auth/logout", "health_check"]:
                app.include_router(module.router, prefix=prefix, dependencies=[Depends(get_current_user)])
            else:
                app.include_router(module.router, prefix=prefix)

def convert_module_path_to_url_prefix(module_info, package):
    partial_relative_path = module_info.name.replace(package + ".", "")
    
    return partial_relative_path.replace(".", "/")
            
include_routers()