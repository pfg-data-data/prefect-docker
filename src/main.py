from prefect import flow, task
from prefect.blocks.system import JSON

json_block = JSON.load('pfg-sheet-credentials')

@task(name ="step 1")
def step1():
    print('dfd')

@flow(name="Do stupid thing")
def print_something():
    step1()
    print(json_block)
