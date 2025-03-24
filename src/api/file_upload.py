from fastapi import APIRouter

router = APIRouter(prefix="/file_upload", tags=["File Upload"])

@router.get('/')
async def file_upload():
    # create logic to store files 
    # if file fails to store then return error
    return {"status": "ok"}
