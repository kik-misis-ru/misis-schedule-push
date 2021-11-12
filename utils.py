import requests
import json
from dotenv import load_dotenv
import  os
from pathlib import Path


Bells = ["bell_1", "bell_2", "bell_3", "bell_4", "bell_5"]
Days = ["day_1", "day_2", "day_3", "day_4", "day_5", "day_6"]


load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
backend_url = os.getenv("BACKEND_APP_URL")

def get_data_for_push(sub: str):
    data={
        'sub':str(sub)
    }
    req = requests.post(backend_url+'get_data_for_push', json = data)
    response = json.dumps(req.json(), indent=2, ensure_ascii=False)
    response_json = json.loads(response)
    return response_json

def get_subs_for_push(hour: int):
    req = requests.get(backend_url+'get_subs_for_push?hour='+str(hour))
    response = json.dumps(req.json(), indent=2, ensure_ascii=False)
    response_json = json.loads(response)
    return response_json


     