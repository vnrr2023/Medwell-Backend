from dotenv import load_dotenv
import os
load_dotenv()
from celery import Celery
from celery.result import AsyncResult
import uuid,json,urllib3,pdfplumber,io
from ai import get_model_response
from prompt_templates import PROMPTS,data_template
from utils import getData,saveDataToMongoDb,saveHealthData
from copy import deepcopy
from db import executeQuery
import os
from messaging import sendStatusMessage

REDIS_CLOUD_URL = os.environ["REDIS_URI"]

celery_app = Celery("tasks", broker=REDIS_CLOUD_URL, backend=REDIS_CLOUD_URL)

celery_app.conf.update(
    task_acks_late=True,  # Ensure tasks are acknowledged only after execution
    worker_prefetch_multiplier=1,  # Distribute tasks evenly among workers
)


@celery_app.task(name="tasks.process_pdf", bind=True)
def process_pdf(self,file, report_id, user_id,email,first_name):
    try:
        http = urllib3.PoolManager()
        temp = io.BytesIO()
        temp.write(http.request("GET", file).data)
        temp.seek(0)
        
        text = ''
        pdf=pdfplumber.open(temp)
        for pdf_page in pdf.pages[:2]:
            text += pdf_page.extract_text()+"\n"

        type_of_report=eval(get_model_response(PROMPTS['type_prompt'],text=text))['type']
        for page in pdf.pages[2:7]:
            text+=page.extract_text()+"\n"

        data_template_copy={}

        if type_of_report=="other":

            data=getData(PROMPTS['other_prompt'],text)
            if not data:
                # self.update_state(state=states.FAILURE, meta={"reason": "Model response failed"})
                raise Exception()

            report_query = "SELECT update_patient_report(%s, %s, %s, %s, %s, %s, %s);"
            report_values = (report_id,data['doctor_name'],data["date_of_report"],data['date_of_collection'],type_of_report,data['summary'],True) 
            executeQuery(report_query,report_values)
            
        else:
            data=getData(PROMPTS['blood_prompt'],text)

            if not data:
                # self.update_state(state=states.FAILURE, meta={"reason": "Model response failed"})
                raise Exception()
            
            sett={"doctor_name","date_of_report","date_of_collection","summary"}
            data_template_copy=deepcopy(data_template)
            for i in data:
                if i not in sett:data_template_copy[i]['value']=data[i] if data[i]!="null" else -1  

            report_query = "SELECT update_patient_report(%s, %s, %s, %s, %s, %s, %s);"
            report_values = (report_id,data['doctor_name'],data["date_of_report"] if data["date_of_report"]!="null" else None ,data['date_of_collection'] if data["date_of_collection"]!="null" else None,type_of_report,data['summary'],True) 
            executeQuery(report_query,report_values)
            report_detail_query = "SELECT insert_patient_report_detail(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            report_detail_values = (
                str(uuid.uuid4()),
                report_id,
                str(data['hemoglobin']) if data['hemoglobin'] != "null" else "-1",
                str(data['rbc_count']) if data['rbc_count'] != "null" else "-1",
                str(data['wbc_count']) if data['wbc_count'] != "null" else "-1",
                str(data['platelet_count']) if data['platelet_count'] != "null" else "-1",
                str(data['pcv']) if data['pcv'] != "null" else "-1",
                str(data['bilirubin_total']) if data['bilirubin_total'] != "null" else "-1",
                str(data['proteins']) if data['proteins'] != "null" else "-1",
                str(data['calcium']) if data['calcium'] != "null" else "-1",
                str(data['blood_urea']) if data['blood_urea'] != "null" else "-1",
                str(data['sr_cholesterol']) if data['sr_cholesterol'] != "null" else "-1",
                json.dumps(data_template_copy)
                )
            executeQuery(report_detail_query,report_detail_values)
            print("stored to db")
        
        saveDataToMongoDb(user_id,data_template_copy,data["date_of_report"],type_of_report,data['summary'])
        saveHealthData(user_id)
        sendStatusMessage("7506375933",file.split("/")[-1],status=True,first_name=first_name)
    except Exception as e:
        print(e)
        self.update_state(state="FAILURE", meta={"error": str(e)})
        sendStatusMessage("7506375933",file.split("/")[-1],status=False,first_name=first_name,)

