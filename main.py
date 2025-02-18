import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

main_url = f'https://ping-admin.com/?a=api&sa=new_task'

def add_task(testing_url: str):
    add_task_url = f'{main_url}&api_key={token}&url={testing_url}'
    response = requests.get(add_task_url)
    return response.json()[0].get('tid', 'error')

def get_info(task_id: int):
    get_info_url = f'{main_url}&api_key={token}&id={task_id}'
    response = requests.get(get_info_url)
    #status_list = lambda x: response.json()[0].get('tasks_logs', 'error')
    return response.json()

print(get_info(2))