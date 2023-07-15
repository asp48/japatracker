import io
import os
import zipfile
from typing import List, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from src import constants, util
from src.configs import env

# If modifying these scopes, delete the file creds.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SUPPORTED_INPUT_FILE_FORMATS = ["txt", "zip"]

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


def get_folder_files(drive_service, folder_id: str):
    response = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        orderBy='createdTime desc',
        fields='files(id, name, trashed)').execute()
    print(response)
    files = []
    for file in response.get('files', []):
        if not file.get('trashed'):
            files.append(file)
    return files


def download_file(drive_service, file_id: str, output_path: str):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()


def get_zip_as_txt_file(zip_file_path: str) -> str:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # TODO: Support multiple files in zip archive
        file_name = zip_ref.namelist()[0]
        with zip_ref.open(file_name) as file:
            file_content = file.read().decode('utf-8')
    os.remove(zip_file_path)
    txt_file_path = zip_file_path.replace("zip", "txt")
    with open(txt_file_path, "w+") as f:
        f.write(file_content)
    return txt_file_path


def load_latest_file_from_drive(folder_id: str, output_path: str):
    if env.mock: return ""
    refresh_token()
    drive_service = build('drive', 'v3', credentials=creds)
    print(f"Searching for files in the folder: {folder_id}")
    files = get_folder_files(drive_service, folder_id)
    if not files: return None
    print(f"Found {len(files)} files.")
    latest_file = files[0]
    file_ext = util.get_file_extension(latest_file.get("name"))
    if file_ext not in SUPPORTED_INPUT_FILE_FORMATS:
        print(f"Unsupported file extension: '{file_ext}'")
        return None
    file_path = os.path.join(output_path, util.get_unique_file_name(constants.INPUT_FILE_PREFIX) + '.' + file_ext)
    print(f"Downloading file: {latest_file.get('id')} to {file_path}")
    download_file(drive_service, latest_file.get('id'), file_path)
    if file_ext == "zip":
        print("Converting zip to txt file...")
        return get_zip_as_txt_file(file_path)
    else:
        return file_path
