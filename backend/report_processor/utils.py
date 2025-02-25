from ai import get_model_response
from datetime import datetime
from prompt_templates import PROMPTS
from langchain_core.output_parsers import JsonOutputParser
from db import COLLECTION,executeQuery
parser=JsonOutputParser()

def getData(prompt,text):
    for i in range(5):
        try:
            resp=get_model_response(prompt,text)
            data=eval(
                resp
            )
            return data
        except:
            try:
                data=parser.parse(resp)
                return data
            except:pass
            if i==4:return {}
            else:pass


def saveDataToMongoDb(user_id,report_data_json,date_of_report,report_type,summary):
    count = COLLECTION.count_documents({"user_id": user_id})
    if count >= 5:
        oldest_doc = COLLECTION.find({"user_id": user_id}).sort("inserted_at", 1).limit(1)
        for doc in oldest_doc:
            COLLECTION.delete_one({"_id": doc["_id"]})

    text=f'''
    Date of report: {date_of_report}
    Report Type: {report_type}
    Summary of report: {summary}
    Report data : {generateReportText(report_data_json)}
    '''
    document = {
        "user_id": user_id,
        "report_data": text,
        "inserted_at": datetime.utcnow()
    }
    COLLECTION.insert_one(document)
    print(f"Report inserted for user in mongodb {user_id}")



def generateReportText(report_data):
    report_text = ""
    for test, details in report_data.items():
        min_val = details['min']
        max_val = details['max']
        unit = details['unit']
        value = details['value']
        if value==-1:continue
        value_text = f"{value} {unit}" if value != -1 else "Not available"
        report_text += f"{test.capitalize()}: Normal range {min_val}-{max_val} {unit}, Current value: {value_text}\n"
    
    return report_text

def saveHealthData(user_id):
    past_history=""
    for report in COLLECTION.find({"user_id":user_id}):
        past_history+=report["report_data"]
    data=getData(PROMPTS["health_summary_prompt"],past_history)
    query = "SELECT update_health_profile(%s, %s, %s);"
    values = (user_id, data["summary"], data['plans'])
    executeQuery(query,values)
    