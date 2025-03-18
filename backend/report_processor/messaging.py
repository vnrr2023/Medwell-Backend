
import requests
import pytz
from datetime import datetime

def sendStatusMessage(to_number,report,status,first_name):
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist)
    human_readable_time = current_time_ist.strftime('%d %B %Y, %I:%M %p')
    if status==True:
        message_body = f'''
    🌟 Hello {first_name},

    ✅ Your report **"{report}"** has been processed successfully! 🎉  

    📅 Processed On: {human_readable_time}  
    📁 Report Name: {report}  

    Thank you for using MedWell! 💙  
    If you need any assistance, feel free to reach out. 😊  
    '''
    else:
        message_body = f'''
    🌟 Hello {first_name},

    ⚠️ We’re sorry, but your report **"{report}"** could not be processed. 😔  

    📅 Attempted On: {human_readable_time}  
    📁 Report Name: {report}  

    🔎 Please check your file format or try uploading again.  
    📬 Need help? Contact our support team here:

    Thank you for trusting MedWell! 💙  
    '''
    resp=requests.post("https://whatsapp-messaging-medwell-api.vercel.app/whatsapp/report-status",json={"phone_number":to_number,"message":message_body})
    print("Message Sent Successfully....")

