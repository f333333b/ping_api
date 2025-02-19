import requests
import os
import time
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

def get_ip_ids():
    """Функция получения ID для всех IP-адресов сервиса ping-admin"""
    get_ip_ids_base_url = f'https://ping-admin.com/?a=api&sa=tm&'
    get_ip_ids_url = f'{get_ip_ids_base_url}&api_key={token}'
    response = requests.get(get_ip_ids_url)
    data = response.json()
    df = pd.DataFrame(data)
    ids = df["id"].tolist()
    with open('ip_ids.txt', 'w') as file:
        for ip in ids:
            file.write(ip + '\n')

def add_task(testing_url: str) -> str:
    """Функция создания задачи"""
    add_task_base_url = f'https://ping-admin.com/?a=api&sa=new_task'
    # способ мониторинга
    algoritm = 1

    # ID точек мониторинга
    with open('ip_ids.txt', 'r') as file:
        ids = file.read().splitlines()
        ids_joined = ','.join(ids)
    tm = ids_joined

    # периодичность проверки (1 = раз в минуту, 2 = раз в 2 минуты и т.д.)
    period = 1

    # периодичность проверки во время ошибки
    period_error = 1

    # проверка на блокировку РКН
    rk = 1

    add_task_url = (f'{add_task_base_url}&api_key={token}&url={testing_url}&period={period}&period_error='
                    f'{period_error}&rk={rk}&algoritm={algoritm}&tm={tm}')
    #print(add_task_url)
    response = requests.get(add_task_url)
    #print(f'response.json()={response.json()}')
    return response.json()

def get_info(task_id: int) -> str:
    """Функция получения статуса задачи"""
    get_info_base_url = f'https://ping-admin.com/?a=api&sa=task_stat&'
    get_info_url = f'{get_info_base_url}&api_key={token}&id={task_id}'
    response = requests.get(get_info_url)
    #print(response.json())
    if response.json()[0].get('tasks_logs', 'error')[0].get('status') == 1:
        return 'success'
    return 'failed'

def delete_task(task_id: int):
    """Фугкция для удаления задачи"""
    delete_task_base_url = f'https://ping-admin.com/?a=api&sa=del_task&'
    delete_task_url = f'{delete_task_base_url}&api_key={token}&id={task_id}'
    response = requests.get(delete_task_url)
    try:
        if response == [{"status":"OK"}]:
            return 'Успешно удалено'
    except Exception as e:
        return e

def check_url(url: str) -> str:
    """Функция проверки ресурса"""
    add_task_result = add_task(url)
    if 'error' in add_task_result:
        print(f'Ошибка: {add_task_result['error']}')
    else:
        task_id = add_task_result[0]['tid']
        status = get_info(task_id)
        if status == 'success':
            time.sleep(5)
            delete_task(task_id)
            return "Проверка успешно завершена"
        else:
            return "Ошибка при получении статуса задачи"

#check_url('https://httpstat.us/503')
check_url('https://ya.ru')
#add_task('https://ya.ru')