from prefect import flow, task

@task(name ="step 1")
def step1():
    print('dfd')

@flow(name="Do stupid thing")
def print_something():
    step1()
    print('he he ho hco')