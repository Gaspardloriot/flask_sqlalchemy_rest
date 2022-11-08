from fastapi import  File, UploadFile
from config.app import app


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile= File(...)):
    return {"filename": file.filename, "test" : "hello from python"}