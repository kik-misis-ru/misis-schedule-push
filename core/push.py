from decimal import DivisionByZero
import re
import requests
from datetime import date, datetime, timedelta
from pathlib import Path
import os
import json
from scheme import *
from requests.api import request
import random
from dotenv import load_dotenv
import uuid
import time
from utils import  get_subs_for_push, get_data_for_push, status_code_success,get_time_frame, TimeFrame
import logging


load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
send_push_url = os.getenv("SEND_PUSH_URL")
auth_sber_url = os.getenv("AUTH_SBER_URL")
client_id_secret_id_base64 = os.getenv("CLIENT_ID_CLIENT_SECRET_BASE64")
project_id_sber_code = os.getenv("PROJECT_ID_SBER_CODE")
time_zone_diff = os.getenv("TIME_ZONE_DIFF")
logging.basicConfig(filename="/logs/mir-misis-push.log", level=logging.INFO)

SECONDS_IN_HOUR = 3600



async def push(data, is_next_day):
    sub = data["sub"]
    templateData = get_data_for_push(sub)
    if templateData["status"] != status_code_success:
        return 
    time_frame = get_time_frame(is_next_day, data["hour"], data["minute"])
    try:
        send_push(sub, templateData, time_frame)
    except DivisionByZero:
        logging.error(f"Error with sending push for sub: {sub}")



def send_push(sub: str, templatedata: PushTemplate, time_frame: TimeFrame):
	data = get_body_for_send_push(sub, templatedata, time_frame)
	headers = {
		'Authorization' : 'Bearer ' + get_auth_token(),
		'Content-type': 'application/json', 'RqUID': get_guid()
		}
	response = requests.post(send_push_url, data = json.dumps(data), headers = headers)
	logging.info(f'Push for sub: {sub} sended.\nResponse text:\n{response.text}\n')

def get_auth_token():
    headers = {
		'Authorization' : 'Basic '+client_id_secret_id_base64,
		'Content-type': 'application/x-www-form-urlencoded', 
		'RqUID': get_guid()
		}
    data = {
		'scope': 'SMART_PUSH'
		}
    response = requests.post(auth_sber_url, data = data, headers = headers)
    return response.json()['access_token']
    


def get_guid():
	guid = str(uuid.uuid4())
	return guid

def get_body_for_send_push(sub: str, templateData: PushTemplate, time_frame: TimeFrame):
	body = {
	"requestPayload": {
		"protocolVersion": "V1",
		"messageId": random.randint(0, 1000000),
		"messageName": "SEND_PUSH",
		"payload": {
			"sender": {
                "projectId" : project_id_sber_code,
				"application" : {
					"appId" : project_id_sber_code,
					"versionId" : project_id_sber_code
				}
			},
			"recipient" : {
				"clientId" : {
					"idType" : "SUB",
					"id" : sub
				}
			},
			"deliveryConfig" : {
				"deliveryMode" : "BROADCAST",
				"destinations" : [{
						"channel" : "COMPANION_B2C",
						"surface" : "COMPANION",
						"templateContent" : {
							"id" : "5be4653f-61ef-47fb-aa08-ddc5ae0d1daa",
							"headerValues" : {
							},
							"bodyValues" : {
							    "day" : templateData["day"],
								"count_lessons" : str(templateData["count_lessons"]),
								"lesson" : templateData["lesson"],
								"start_lesson_info": templateData["start_lesson_info"],
                                "start_time" :templateData["start_time"]
							},
							"mobileAppParameters" : {
							},
							"timeFrame" : {
							 	"startTime" : time_frame.start_time.strftime("%H:%M:%S"), 
							 	"finishTime" : time_frame.finish_time.strftime("%H:%M:%S"),  
							 	"timeZone" : "GMT+03:00",
							 	"startDate" : time_frame.start_date.strftime("%Y-%m-%d"), 
							 	"endDate" : time_frame.end_date.strftime("%Y-%m-%d"), 
							 }
						}
					}
				]
			}
		}
	}
	}
	return body


async def run_push():
    while True:
        try:
            start = datetime.now()
            push_hour = datetime.now().hour + 1 +int(time_zone_diff)
            is_next_day = False
            if push_hour > 23:
                push_hour = push_hour % 24
                is_next_day = True
            logging.info(f"Start sending push for hour: {push_hour}")
            subs = get_subs_for_push(push_hour)
            if subs["status"] == status_code_success:
                for sub in subs["data"]:
                   await push(sub, is_next_day)
        except DivisionByZero:
            logging.error(f"Error with sending pushes for hour: {push_hour}")
        delta = datetime.now() - start
        time.sleep(SECONDS_IN_HOUR - delta.total_seconds())

