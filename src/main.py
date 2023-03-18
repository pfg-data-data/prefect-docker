#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Dataframe
import pandas as pd
import numpy as np

# Prefect
from prefect import flow, task

# Time
from datetime import date, timedelta
from time import gmtime, strftime

import datetime
import time


# In[2]:


# Connect to Google Sheets
sheet_list_url          = '1c-fmeZbQGs2jESqCH9lZlm80cH2CR9VEHvWNwFbsjeo'

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("pfg_sheet_credentials.json", scope)
gc = gspread.authorize(credentials)

# Create sheet function
def pd_extract_sheet_data(destination_database_url, destination_sheet):
    # open sheet and extract all data
    wks = gc.open_by_key(destination_database_url).worksheet(destination_sheet)
    data = wks.get_all_records()
    return data

def np_extract_sheet_data(destination_database_url, destination_sheet):
    # open sheet and extract all data
    wks = gc.open_by_key(destination_database_url).worksheet(destination_sheet)
    array = np.array(wks.get_all_values()[1:])
    list_data = array.tolist()
    return list_data

def remove_sheet_data(destination_database_url, destination_sheet):
    wks = gc.open_by_key(destination_database_url).worksheet(destination_sheet)
    wks.batch_clear(['A:Z'])
    # wait before move to next task
    time.sleep(5)
    
def insert_all_sheet_data(data_to_load, destination_database_url, destination_sheet):
    wks = gc.open_by_key(destination_database_url).worksheet(destination_sheet)
    wks.update('A1', [data_to_load.columns.values.tolist()] + data_to_load.values.tolist())
    # wait before move to next task
    time.sleep(1 * 60)

#-----------


# In[3]:


@task(name                = "Step 1: Extract",
      retries             = 10, 
      retry_delay_seconds = 60)
def extract():
    # Lấy data từ sheet_list để có list của các sheet từ POS
    df_sheet_list = pd.DataFrame(pd_extract_sheet_data(sheet_list_url, 'sheet_list'))
    
    # Vào từng url để quét data từ 6 sheet
    all_data = []
    for i in df_sheet_list['google_sheet_id']:
        data = np_extract_sheet_data(i, 'PosSheets(duplicate_orders)')
        print(type(data))
        all_data.extend(data)
        
    # Convert all_data thành 1 big dataframe
    df_all_data = pd.DataFrame(all_data, columns = ['ID', 'Full Order ID', 'Order status','Tracking number','Carrier','Status','Number of items',
                                        'Customer','Phone number', 'Products list', 'Address','Creator', 'Create at','Total price','COD','Warehouse'])
    
    return df_all_data


# In[4]:


@task(name                = "Step 2: Transform",
      retries             = 10, 
      retry_delay_seconds = 60)
def transform(df_all_data):
    # tạo thêm trường dữ liệu
    shop_id = []
    for i in df_all_data['Full Order ID']:
        i = i.split('O', 1)[0][1:]
        shop_id.append(i)

    df_all_data['shop_id'] = shop_id

    phone_number = []
    for i in df_all_data['Phone number']:
        phone_number.append(str(i))
    df_all_data['Phone number'] = phone_number

    create_at = []
    for i in df_all_data['Create at']:    
        create_at.append(i[-4:] + '-' +  i[-7:-5] + '-' + i[-10:-8] + ' ' + i[:5])
    df_all_data['Create at'] = create_at


    # lọc đơn trùng dựa trên số điện thoại và sắp xếp theo số điện thoại, ngày tháng
    df_all_data = df_all_data[df_all_data.duplicated(subset=['Phone number'], keep = False)].sort_values(by= ['Create at'], ascending=False) #'Phone number', 
    df_all_data = df_all_data[df_all_data['Full Order ID'] != '']

    # sửa cột ngày tháng thành text để load lên sheet
    create_at = []
    for i in df_all_data['Create at']:
        create_at.append(str(i))
    df_all_data['Create at'] = create_at
    
    return df_all_data


# In[5]:


@task(name                = "Step 3: Load",
      retries             = 10, 
      retry_delay_seconds = 60)
def load(df_all_data):
    remove_sheet_data(sheet_list_url, 'test')
    insert_all_sheet_data(df_all_data, sheet_list_url, 'test')


# In[6]:


@flow(name                = "Leto Double order",
      retries             = 10, 
      retry_delay_seconds = 60)
def leto_double_order():
    df_all_data = extract()
    df_all_data = transform(df_all_data)
    load(df_all_data)


# In[ ]:


leto_double_order()

