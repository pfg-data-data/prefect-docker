# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Dataframe
import pandas as pd
import numpy as np

# -----------------------------
from prefect import flow, task

from prefect.blocks.system import JSON

json_block = JSON.load("pfg-sheet-credentials")
a= json_block.value

@task(name ="step 1")
def step1():
    print('dfd')

    
@flow(name="Do stupid thing")
def print_something():
    step1()


    print(a)
    print(type(a))
    sheet_list_url          = '1c-fmeZbQGs2jESqCH9lZlm80cH2CR9VEHvWNwFbsjeo'

    scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(a, scope)
    gc = gspread.authorize(credentials)
