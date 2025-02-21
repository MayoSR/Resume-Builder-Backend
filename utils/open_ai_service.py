from openai import OpenAI # type: ignore
from utils.google_services import copy_google_doc, update_google_doc, extract_lines_from_doc, get_docs_service
from random import randint
import ast
import os
import time
import datetime
from dotenv import load_dotenv # type: ignore
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
)

CHATGPT_DEVELOPER_PROMPT = os.getenv("CHATGPT_DEVELOPER_PROMPT")
CHATGPT_USER_PROMPT = os.getenv("CHATGPT_USER_PROMPT")

def get_openai_response(resume_content, job_desc):
    return client.chat.completions.create(
            messages=[
                {
                    "role": "developer", 
                    "content": CHATGPT_DEVELOPER_PROMPT},
                {
                    "role": "user", 
                    "content": CHATGPT_USER_PROMPT.format(
                        resume_content=resume_content,
                        job_desc=job_desc
                    )
                }
            ],        
            model="gpt-4o",
        )
    
    

    
def process_openai_response(json_data):
    resume_content = extract_lines_from_doc(json_data['documentId'])
    fontFamily = json_data['fontFamily']
    companyName = json_data['companyName']
    job_desc = json_data['jobDesc']
    
    service = get_docs_service()
    response = get_openai_response(resume_content, job_desc)

    parsed_response = response.choices[0].message.content
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    copied_doc_id = copy_google_doc(json_data['documentId'], f"Resume for {companyName}-{timestamp}")
    update_google_doc(service, copied_doc_id, ast.literal_eval(str(parsed_response.lstrip('```json\n').rstrip('```\n'))), fontFamily)