from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import tempfile
import secrets
import subprocess
import os

from utils import save_temp_file, create_post_script_file

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/upload")
async def upload_files(pdf_file: UploadFile = File(...), xml_file: UploadFile = File(...),xml_file_name=None):
    session_id = secrets.token_hex(8)
    pdf_file_path = await save_temp_file(await pdf_file.read(), '.pdf', session_id)
    xml_file_path = await save_temp_file(await xml_file.read(), '.xml', session_id)
    ps_file = await create_post_script_file(xml_file_path,  session_id,xml_file_name=xml_file_name)
    result_file_path = os.path.join(tempfile.mkdtemp(), session_id) + '.pdf'
    command = f"gs -sDEVICE=pdfwrite -dNOSAFER -dPDFA=3 -sColorConversionStrategy=RGB -dPDFACompatibilityPolicy=2 -o {result_file_path} {pdf_file_path} {ps_file} -dDEBUG"
    subprocess.run(command, shell=True)
    
    print(result_file_path)
    return FileResponse(result_file_path, filename="result.pdf")