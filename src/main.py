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



------------
from prefect.blocks.system import JSON

json_block = JSON.load("pfg-sheet-credentials")
# In[2]:

@task(name ="step 1")
def step1():
    print('dfd')

@flow(name="Do stupid thing")
def print_something():
    step1()
    print(json_block)


