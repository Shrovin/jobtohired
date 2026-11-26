import csv
import io
import json
from datetime import datetime, timezone

import gspread
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, ContentSettings

# Address of the Key Vault that holds the secrets
KEY_VAULT_URL = "https://kv-jobtohired26.vault.azure.net/"

# Address of the data lake and the raw (bronze) container
STORAGE_ACCOUNT_URL = "https://jobtohiredlake26.blob.core.windows.net"
BRONZE_CONTAINER = "bronze"

# Read-only access to Google Sheets (least privilege)
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_secrets(credential):
    """Fetch the robot's key and the sheet ID from Key Vault."""
    client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
    sa_key = json.loads(client.get_secret("google-sa-key").value)
    sheet_id = client.get_secret("sheet-id").value
    return sa_key, sheet_id


def read_responses(sa_key, sheet_id):
    """Return every row of the responses tab, including the header row."""
    gc = gspread.service_account_from_dict(sa_key, scopes=GOOGLE_SCOPES)
    worksheet = gc.open_by_key(sheet_id).sheet1
    return worksheet.get_all_values()


def rows_to_csv(rows):
    """Turn the rows into CSV text."""
    buffer = io.StringIO()
    csv.writer(buffer).writerows(rows)
    return buffer.getvalue()


def save_to_bronze(credential, csv_text):
    """Save a new, timestamped snapshot in bronze. Never overwrites."""
    now = datetime.now(timezone.utc)
    blob_path = (
        f"survey_responses/ingest_date={now:%Y-%m-%d}/"
        f"responses_{now:%Y%m%dT%H%M%SZ}.csv"
    )
    service = BlobServiceClient(STORAGE_ACCOUNT_URL, credential=credential)
    blob = service.get_blob_client(container=BRONZE_CONTAINER, blob=blob_path)
    blob.upload_blob(
        csv_text.encode("utf-8"),
        overwrite=False,
        content_settings=ContentSettings(content_type="text/csv"),
    )
    return blob_path


if __name__ == "__main__":
    credential = DefaultAzureCredential()
    sa_key, sheet_id = get_secrets(credential)
    rows = read_responses(sa_key, sheet_id)
    print(f"Columns in the sheet: {len(rows[0])}")
    print(f"Responses found: {len(rows) - 1}")
    path = save_to_bronze(credential, rows_to_csv(rows))
    print(f"Saved to bronze: {path}")