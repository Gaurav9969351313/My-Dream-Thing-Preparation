import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('annular-will.json', scope)
client = gspread.authorize(creds)

doc = client.open_by_url('https://docs.google.com/spreadsheets/d/17YocQbRYtkRDxsc4qhjWj_2HQXWEAkildZhRx2bsDRA/edit?usp=sharing')

worksheet = doc.worksheet('GetHistoricalData')

list_of_dicts = worksheet.get_all_records()

df = pd.DataFrame(worksheet.get_all_values())
print(df.head(10))

