import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    # Try to open the sheet, if not found create it
    try:
        sheet = client.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = client.create(sheet_name)

        # VERY IMPORTANT: share the sheet with your service account email so it's visible in Drive
        service_account_email = creds.service_account_email
        sheet.share(service_account_email, perm_type='user', role='writer')

    return sheet


import pandas as pd

def log_data(sheet, df, tab_name="Trades"):
    try:
        worksheet = sheet.worksheet(tab_name)
    except:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="20")

    worksheet.clear()

    # ✅ Step 1: Remove infinities and NaNs
    df = df.replace([float("inf"), float("-inf")], "").fillna("")

    # ✅ Step 2: Make sure columns are NOT nested
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(map(str, col)) for col in df.columns]
    else:
        df.columns = df.columns.astype(str)

    # ✅ Step 3: Make sure ALL cell values are stringified scalars
    def clean_cell(x):
        return str(x) if isinstance(x, (list, dict, tuple, pd.Timestamp)) else x

    df = df.map(clean_cell).astype(str)


    # ✅ Step 4: Combine header + data into 2D list
    values = [list(df.columns)] + df.values.tolist()

    # ✅ Step 5: Write to sheet
    try:
        worksheet.update("A1", values)
    except Exception as e:
        print("❌ Google Sheets update failed:", e)
        print("Check if values[0] is a list of plain strings:", values[0])
        print("Check if values[1:] is a list of lists:", values[1:])
        raise e