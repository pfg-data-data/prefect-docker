# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import ast

# Dataframe
import pandas as pd
import numpy as np

# -----------------------------
from prefect import flow, task
from prefect.blocks.system import JSON

json_block = JSON.load('pfg-sheet-credentials')


# -----------

from prefect.blocks.system import Secret

secret_block = Secret.load("sheet-api")

# Access the stored secret

with open(json_block) as user_file:
    parsed_json = json.load(user_file)



# # Connect to Google Sheets
# sheet_list_url          = '1c-fmeZbQGs2jESqCH9lZlm80cH2CR9VEHvWNwFbsjeo'

# scope = ['https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive"]

# credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_block.json(), scope)
# gc = gspread.authorize(credentials)

# # Create sheet function
# def pd_extract_sheet_data(destination_database_url, destination_sheet):
#     # open sheet and extract all data
#     wks = gc.open_by_key(destination_database_url).worksheet(destination_sheet)
#     data = wks.get_all_records()
#     return data


@task(name ="step 1")
def step1():
    print('dfd')

# @task(name ="step 2")
# def step2():
#     pd_extract_sheet_data(sheet_list_url, 'test')
    
@flow(name="Do stupid thing")
def print_something():
    step1()
    a = json_block.json()
    print(parsed_json)
    print('secret')
    print(secret_block.get())
    print('___________________')
    print(json_block['value'])
    print(type(json_block))
    print('___________________')
    print(a)
    print('___________________')
    print(type(a))
    sheet_list_url          = '1c-fmeZbQGs2jESqCH9lZlm80cH2CR9VEHvWNwFbsjeo'

    scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(a, scope)
    gc = gspread.authorize(credentials)
