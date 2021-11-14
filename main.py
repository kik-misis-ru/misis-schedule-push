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
from utils import Days, Bells, get_subs_for_push, get_data_for_push
# mongo_repository = MongoRepository()
import asyncio


load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
send_push_url = os.getenv("SEND_PUSH_URL")
auth_sber_url = os.getenv("AUTH_SBER_URL")
client_id_secret_id_base64 = os.getenv("CLIENT_ID_CLIENT_SECRET_BASE64")
project_id_sber_code=os.getenv("PROJECT_ID_SBER_CODE")
time_zone_diff = os.getenv("TIME_ZONE_DIFF")

status_code_success = "1"
status_code_not_found = "-1"
status_code_error= "-2"




async def push(data, is_next_day):
	sub = data["sub"]
	templateData = get_data_for_push(sub)
	if templateData["status"] != status_code_success:
		return 
	start_time = datetime.today()
	start_date = datetime.today()
	end_date = start_date
	start_time = start_time.replace(hour=data['hour'], minute=data['minute'], second=0, microsecond=0)
	finish_time = start_time + timedelta(minutes=1)
	if is_next_day:
		start_time = start_time + timedelta(hours = 24)
		start_date = start_date + timedelta(hours = 24)
		finish_time = finish_time + timedelta(hours = 24)
		end_date = end_date + timedelta(hours = 24)

	send_push(sub, templateData, start_time, finish_time, start_date, end_date)

async def run_push():
	while(True):
		start = datetime.now()
		push_hour = datetime.now().hour + 1 + int(time_zone_diff)
		is_next_day = False
		if push_hour > 23:
			push_hour = push_hour % 24
			is_next_day = True
		subs = get_subs_for_push(push_hour)
		for sub in subs:
			await push(sub, is_next_day)
		delta = datetime.now() - start
		print("time:",3600 - delta.total_seconds())
		print("time:",datetime.now())
		time.sleep(3600 - delta.total_seconds())


def send_push(sub: str, templateData: PushTemplate, start_time: datetime, finish_time: datetime, start_date: date, end_date:date):
    data = get_body_for_send_push(sub, templateData, start_time, finish_time, start_date, end_date)
    headers={'Authorization': 'Bearer '+get_auth_token(), 'Content-type': 'application/json', 'RqUID': get_guid()}

    response = requests.post(send_push_url, data=json.dumps(data), headers=headers)
    
    print(response.text)

def get_auth_token():
    headers={'Authorization': 'Basic '+client_id_secret_id_base64, 'Content-type': 'application/x-www-form-urlencoded', 'RqUID': get_guid()}
    data={'scope': 'SMART_PUSH'}
    response = requests.post(auth_sber_url, data=data, headers=headers)
    print(response.json()['access_token'])
    return response.json()['access_token']
    


def get_guid():
	guid = str(uuid.uuid4())
	return guid

def get_body_for_send_push(sub: str, templateData: PushTemplate, start_time: datetime, finish_time: datetime, start_date: date, end_date:date):
	print("start_time",start_time.strftime("%H:%M:%S"))
	print("finish_time", finish_time.strftime("%H:%M:%S"))
	print("start_date", start_time.strftime("%Y-%m-%d"))
	print("end_date", end_date.strftime("%Y-%m-%d"))
	body = {
	"requestPayload": {
		"protocolVersion": "V1",
		"messageId": random.randint(0, 1000000),
		"messageName": "SEND_PUSH",
		"payload": {
			"sender": {
                "projectId":project_id_sber_code,
				"application": {
					"appId": project_id_sber_code,
					"versionId": project_id_sber_code
				}
			},
			"recipient": {
				"clientId": {
					"idType": "SUB",
					"id": sub
				}
			},
			"deliveryConfig": {
				"deliveryMode": "BROADCAST",
				"destinations": [{
						"channel": "COMPANION_B2C",
						"surface": "COMPANION",
						"templateContent": {
							"id": "935f93f9-002b-4265-88ec-75de24ce6a99",
							"headerValues": {
							},
							"bodyValues": {
							    "day": templateData["day"],
								"count_lessons": str(templateData["count_lessons"]),
								"lesson": templateData["lesson"],
                                "start_time":templateData["start_time"]
							},
							"mobileAppParameters": {
							},
							"timeFrame": {
							 	"startTime": start_time.strftime("%H:%M:%S"), #(datetime.now()+timedelta(minutes=1)).strftime("%H:%M:%S"),
							 	"finishTime": finish_time.strftime("%H:%M:%S"), #(datetime.now()+timedelta(minutes=2)).strftime("%H:%M:%S"), 
							 	"timeZone": "GMT+03:00",
							 	"startDate": start_date.strftime("%Y-%m-%d"), #'2021-11-12',
							 	"endDate": end_date.strftime("%Y-%m-%d"), #'2021-11-12',
							 }
						}
					}
				]
			}
		}
	}
	}
	return body

asyncio.run(run_push())