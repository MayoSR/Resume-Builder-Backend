# Resume Builder: Auto-Updating Your Google Docs with Job Descriptions

## Overview
This project is a resume builder that automatically updates your Google Docs with any job description provided. It utilizes:
- **Google Drive API & Google Docs API:** For managing and updating documents.
- **OpenAI API:** For generating resume content.
- **Service Account Authentication:** To securely interact with Google APIs.
- **Python Virtual Environment:** To manage project dependencies.
- Configuration is managed via a **.env** file (initially provided as `.env.test`).

This document outlines how to set up and run the application.

## Prerequisites
- **Python 3.7+** installed on your system.
- A **Google Cloud account**.
- A **Google Cloud project** with the following APIs enabled:
  - [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
  - [Google Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com)
  - ![Frame 2 (1)](https://github.com/user-attachments/assets/be70ae4e-05a7-42b7-bd28-39171d9aac63)

- A **Service Account** with its JSON key file  
  (see [Google Cloud Service Account Setup](https://cloud.google.com/iam/docs/service-accounts) for instructions).
  - Ensure you give **Owner** privileges to the service account.
  - ![Screenshot 2025-02-23 153925](https://github.com/user-attachments/assets/c150c630-6ef3-4777-8113-138ad4e26feb)

- An **OpenAI API Key** (sign up or log in at [OpenAI](https://platform.openai.com/)).
  - [OpenAI Keys](https://platform.openai.com/settings/organization/api-keys)
  -  ![Screenshot 2025-02-23 153744](https://github.com/user-attachments/assets/16264859-cbf2-4e15-b719-2058fb14d189)

- Approximately \$10 budget for API usage (each resume generation costs around 5 cents, allowing about 200 resumes per \$10).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MayoSR/Resume-Builder-Backend.git
cd Resume-Builder-Backend
```
### 2. Create and Activate a Python Virtual Environment
```bash
# Create a virtual environment named "venv"
python -m venv venv
```

#### Activate the virtual enviornment
```bash
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
-  Rename the file named .env.test to .env and fill in the keys as mentioned
-  Copy and Paste your service account .json file in the same location as your 

### 5. Run the application with
```bash
python app.py
```

## Additional Resources
- Google Cloud Console: https://console.cloud.google.com/
- Service Account Documentation: Google Cloud Service Account Setup
- OpenAI API Documentation: https://platform.openai.com/docs/
- Python Virtual Environments: https://docs.python.org/3/tutorial/venv.html

## Troubleshooting
- Environment Variables: Ensure the .env file is correctly named and located in the project's root directory.
- Google API Authentication: Verify the path to your service account JSON file and confirm permissions.
- Dependencies: Update your Python package manager and reinstall dependencies if issues occur.
- Additional Help: Consult the official documentation for Google APIs and OpenAI for further assistance.
## License
This project is licensed under the MIT License.
