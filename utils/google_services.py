
from google.oauth2 import service_account # type: ignore
from googleapiclient.discovery import build # type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
USER_EMAIL = os.getenv("USER_EMAIL")

def get_docs_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("docs", "v1", credentials=creds)

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def extract_lines_from_doc(id):
    doc = get_docs_service().documents().get(documentId=id).execute()
    modifiable_lines = []

    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            node = element
            chatgpt_token_parse = "".join(
                el.get("textRun", {}).get("content", "")
                for el in node.get("paragraph", {}).get("elements", [])
            )
            modifiable_lines.append({
                "text": chatgpt_token_parse,
                "startIndex": node.get("startIndex"),
                "endIndex": node.get("endIndex")
            })
    
    print("Extracted lines:", doc)
    
    return modifiable_lines

def copy_google_doc(template_id, new_title):
    U1_EMAIL = USER_EMAIL
    drive_service = get_drive_service()
    copied_file = drive_service.files().copy(
        fileId=template_id,
        body={'name': new_title}
    ).execute()
    
    new_file_id = copied_file.get('id')
    print(f"New copy created with ID: {new_file_id}")
    
    print(f"Sharing new file with {U1_EMAIL}...")
    permission_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': U1_EMAIL
    }
    drive_service.permissions().create(
        fileId=new_file_id,
        body=permission_body
    ).execute()
    print("Shared successfully.")
    
    return new_file_id

def update_google_doc(service, document_id, updates, fontFamily):

    updates_sorted = sorted(updates, key=lambda u: u["start"], reverse=True)

    requests = []

    for i, update in enumerate(updates_sorted):
        start_index = update.get("start")
        end_index = update.get("end")
        new_text = update.get("line", "").rstrip('\n')
        text_style = update.get("textStyle", "")

        if start_index is None or end_index is None:
            print(f"Skipping update #{i}: Missing start or end index.")
            continue

        if start_index >= end_index:
            print(f"Skipping update #{i}: Invalid range (start={start_index}, end={end_index}).")
            continue

        requests.append({
            "deleteContentRange": {
                "range": {
                    "startIndex": start_index,
                    "endIndex": end_index - 1
                }
            }
        })

        requests.append({
            "insertText": {
                "location": {"index": start_index},
                "text": new_text
            }
        })
        
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": start_index,
                    "endIndex": start_index + len(new_text)
                },
                "textStyle": {
                    "weightedFontFamily": {
                        "fontFamily": fontFamily
                    },
                },
                "fields": "weightedFontFamily"
            }
        })

    if not requests:
        print("No valid requests to process.")
        return
    
    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests}
    ).execute()

    print("Document updated successfully!")