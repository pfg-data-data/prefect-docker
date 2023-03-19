# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
from prefect import flow, task
from prefect.blocks.system import JSON

json_block = JSON.load('pfg-sheet-credentials')


# Connect to Google Sheets
# sheet_list_url          = '1c-fmeZbQGs2jESqCH9lZlm80cH2CR9VEHvWNwFbsjeo'

# scope = ['https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive"]

# credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_block, scope)
# gc = gspread.authorize(credentials)




@task(name ="step 1")
def step1():
    print('dfd')

    
    
    
    
    
@flow(name="Do stupid thing")
def print_something():
    step1()
    print(type(d))
