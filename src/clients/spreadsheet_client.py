import os
from typing import List, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src import constants
# If modifying these scopes, delete the file creds.json.
from src.configs import env

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']

if not os.path.exists('secrets/credentials.json'):
    raise Exception("Could not find credentials to connect Google APIs. Please add it under secrets.")

creds = None

if os.path.exists('secrets/token.json'):
    creds = Credentials.from_authorized_user_file('secrets/token.json', SCOPES)


def refresh_token():
    global creds
    # The file creds.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('secrets/token.json', 'w') as token:
            token.write(creds.to_json())


def create_new_spreadsheet(name: str, folder_id: str) -> str:
    if env.mock: return ""
    refresh_token()
    drive_service = build('drive', 'v3', credentials=creds)
    file_meta = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [folder_id]
    }
    print(f"Creating new file: {name} under folder-id {folder_id}...")
    sheet = drive_service.files().create(body=file_meta, fields='id').execute()
    return sheet['id']


def write_new_sub_sheet(sheet_id: str, name: str, data: List[List[Any]], headers: List[str]):
    if env.mock: return ""
    refresh_token()
    sheets = build('sheets', 'v4', credentials=creds).spreadsheets()
    add_sheet_request = {
        "requests": {
            "addSheet": {
                "properties": {
                    "title": name
                }
            }
        }
    }
    print(f"Adding a new sub sheet: {name} under {sheet_id}...")
    sheets.batchUpdate(spreadsheetId=sheet_id, body=add_sheet_request).execute()
    print(f"Writing data to new sub-sheet: {name} ")
    data = [headers] + data
    range_name = '{}!A1:{}'.format(name, chr(ord('A') + len(headers)))
    write_to_sheet(sheets, sheet_id, range_name, data)


def append_to_sheet(sheet_id: str, data: List[List[Any]], headers: List[str],
                    sub_sheet_name: str = constants.DEFAULT_SHEET_NAME):
    if env.mock: return ""
    refresh_token()
    sheets = build('sheets', 'v4', credentials=creds).spreadsheets()
    print(f"Fetching sheet: {sheet_id} to know the current number of rows")
    result = sheets.values().get(spreadsheetId=sheet_id, range=sub_sheet_name).execute()
    row_count = len(result.get('values', []))
    print(f"Row count: {row_count}")
    if row_count == 0:
        print("Adding headers at the beginning of data")
        data = [headers] + data
    range_name = '{}!A{}:{}'.format(sub_sheet_name, row_count + 1, chr(ord('A') + len(headers)))
    write_to_sheet(sheets, sheet_id, range_name, data)


def write_to_sheet(sheets, sheet_id: str, range_name: str, data: List[List[Any]]):
    body = {
        'values': data
    }
    sheets.values().update(spreadsheetId=sheet_id, range=range_name, valueInputOption='RAW',
                           body=body).execute()
