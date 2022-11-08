import os
from fastapi import  File, UploadFile
from config.app import app
import pandas as pd


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile= File(...)):
    contents = await file.read()   
    output = open('test.xls', 'wb')
    output.write(contents)
    output.close()
    df = pd.read_excel('./test.xls')
    print(df.head())
    os.remove('test.xls')



    return {"filename": file.filename, "test" : "hello from python"}