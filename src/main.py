from prefect import flow, task
from prefect.blocks.system import JSON

json_block = JSON.load('pfg-sheet-credentials')

import json
d = json.loads(json_block)

@task(name ="step 1")
def step1():
    print('dfd')

@flow(name="Do stupid thing")
def print_something():
    step1()
    print(type(d))
