import logging
import requests
import json
from dotenv import load_dotenv
import  os
from pathlib import Path
from scheme import TimeFrame
from datetime import datetime, timedelta


Bells = ["bell_1", "bell_2", "bell_3", "bell_4", "bell_5"]
Days = ["day_1", "day_2", "day_3", "day_4", "day_5", "day_6"]

status_code_success = "1"
status_code_not_found = "-1"
status_code_error = "-2"


load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
backend_url = os.getenv("BACKEND_APP_URL")

def get_data_for_push(sub: str):
    data={
        'sub':str(sub)
    }
    try:
        req = requests.post(backend_url+'get_data_for_push', json = data)
        if req.status_code!=200:
            return {"status": status_code_error}
        response = json.dumps(req.json(), indent=2, ensure_ascii=False)
        response_json = json.loads(response)
        return response_json
    except requests.exceptions.ConnectionError:
        logging.error(f"Api: {backend_url} is not available")
        return {"status": status_code_error}

def get_subs_for_push(hour: int):
    try:
        req = requests.get(backend_url+'get_subs_for_push?hour='+str(hour))
        if req.status_code!=200:
            return {"status": status_code_error}
        response = json.dumps(req.json(), indent=2, ensure_ascii=False)
        response_json = json.loads(response)
        response_json["status"] = status_code_success
        return response_json
    except requests.exceptions.ConnectionError:
        logging.error(f"Api: {backend_url} is not available")
        return {"status": status_code_error}
    

def get_time_frame(is_next_day: bool, hour: int, minute = int, second = 0, microsecond = 0):
    start_time = datetime.today()
    start_date = datetime.today()
    end_date = start_date
    start_time = start_time.replace(hour = hour, minute = minute, second = 0, microsecond = 0)
    finish_time = start_time + timedelta(minutes = 1)

    if is_next_day:
        start_time = start_time + timedelta(hours = 24)
        start_date = start_date + timedelta(hours = 24)
        finish_time = finish_time + timedelta(hours = 24)
        end_date = end_date + timedelta(hours = 24)
    return TimeFrame(start_time, finish_time, start_date, end_date)



     