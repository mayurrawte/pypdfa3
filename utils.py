import tempfile
from constant import ps_content_template
from fastapi import UploadFile
import subprocess


xml_path = '/home/thepsygeek/zugferd/sample.xml'
xml_filename = 'sample.xml'




async def save_temp_file(upload_file: UploadFile, file_extension: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
        # Save the file
        temp_file.write(await upload_file.read())
        temp_file_path = temp_file.name
    return temp_file_path


import os

async def save_temp_file(file_data: bytes, file_extension: str, folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False, dir=folder) as temp_file:
        temp_file.write(file_data)
        temp_file_path = temp_file.name
    return temp_file_path


async def create_post_script_file(xml_file_path: str, session_id):
     content = ps_content_template.format(xml_path=xml_file_path, xml_filename='invoice.xml', gs_version=get_gs_version())
     return await save_temp_file(content.encode('utf-8'), '.ps', session_id)

def get_gs_version():
    try:
        gs_version = subprocess.check_output(["gs", "--version"]).strip().decode()
        return gs_version
    except subprocess.CalledProcessError:
        return "Ghostscript not found"