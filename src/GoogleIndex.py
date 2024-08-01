# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/home/vladvons/Downloads/sublime-shift-414509-2ec227eafe7f.json'
assert(os.path.exists(SERVICE_ACCOUNT_FILE))

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/indexing']

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service
service = build('indexing', 'v3', credentials=credentials)

# URL to be indexed
url = 'https://1x1.com.ua/product/dell_precision_3620_tower_e3-1220v5_16gb_256gb_ssd_r5_340x_2gb_t2'

# Create the request body
body = {
    'url': url,
    'type': 'URL_UPDATED'
}

# Send the request
response = service.urlNotifications().publish(body=body).execute()
print(response)
