import json,os
import pandas as pd
from sqlalchemy import create_engine,text as to_sql_text
from utils import getData,setData
from urllib.parse import quote
from datetime import datetime
from colorama import Fore

DB_NAME=os.environ["DB_NAME"]
DB_USER=os.environ["DB_USER"]
PASSWORD=os.environ["DB_PASSWORD"]
DB_HOST=os.environ["DB_HOST"]
DB_PORT=os.environ["DB_PORT"]


encoded_password = quote(PASSWORD)
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:6543/{DB_NAME}",pool_size=10, max_overflow=5, pool_recycle=1800)
conn=engine.connect()
print(Fore.GREEN+"Connected to Db Successfully"+Fore.WHITE)

queries=json.load(open("queries.json"))
dashboard_queries=json.load(open("dashboard_queries.json"))

class Patient:
    @staticmethod
    def provide_health_check_data(user_id):
        data=getData(f"health_check:{user_id}")
        if data["status"]:return data["data"]
        df=pd.read_sql_query(to_sql_text(queries["health_check"].format(user_id=user_id)),con=conn)
        count=int(df.num_reports.iloc[0])
        if count<4:return {"status":False,"count":count}
        df.replace("-1",None,inplace=True)
        df['submitted_at'] = df['submitted_at'].astype(str)
        data=df.iloc[:, 1:12].to_dict("list")
        avg_data=df.iloc[0, 12:].to_dict()
        resp={'avg_data':avg_data,'data':data,'status':True}
        setData(f"health_check:{user_id}",resp)
        return resp
        
    # provides the overall expense and most recent 10 expenses
    @staticmethod
    def provide_expense_data(user_id):
        data=getData(f"expense_data:{user_id}")
        if data["status"]:return data["data"]
        df=pd.read_sql_query(to_sql_text(queries["expense_list"].format(user_id=user_id)),con=conn)
        total_exp=df.total_expense.iloc[0]
        df['expense_date'] = df['expense_date'].astype(str)
        data=df.iloc[:, 1:].to_dict("records")
        resp={"overall_expense":total_exp,"expenses":data}
        setData(f"expense_data:{user_id}",resp)
        return resp

        
    # provides analytical data for expense dashboard
    @staticmethod
    def provide_expense_dashboard(user_id):
        data=getData(f"expense_dashboard:{user_id}")
        if data["status"]:return data["data"]
        df=pd.read_sql_query(sql=to_sql_text(queries["expense_per_type"].format(user_id=user_id)),con=conn)
        expenses_per_type=df.to_dict("list")
        df=pd.read_sql_query(sql=to_sql_text(queries["expense_trend"].format(user_id=user_id)),con=conn)
        expense_trend=df.to_dict("list")
        df=pd.read_sql_query(sql=to_sql_text(queries["expenses_per_month"].format(user_id=user_id)),con=conn)[["month_name","expenses"]]
        expenses_per_month=df.to_dict("list")
        df=pd.read_sql_query(sql=to_sql_text(queries["expenses_per_year"].format(user_id=user_id)),con=conn)[["year","expenses"]]
        expenses_per_year=df.to_dict("list")
        df=pd.read_sql_query(sql=to_sql_text(queries["expense_per_month_per_type"].format(user_id=user_id)),con=conn)
        grouped_df = df.groupby(by="month")
        expenses_per_month_per_type=[]
        for month,df in grouped_df:
            month_data = {
                "month": month,
                "data": df[["expense_type","expenses"]].to_dict("list")
            }
            expenses_per_month_per_type.append(month_data)
        df=pd.read_sql_query(sql=to_sql_text(queries["expenses_per_year_per_type"].format(user_id=user_id)),con=conn)
        grouped_df = df.groupby(by="year")
        expenses_per_year_per_type=[]
        for year,df in grouped_df:
            year_data = {
                "month": year,
                "data": df[["expense_type","expenses"]].to_dict("list")
            }
            expenses_per_year_per_type.append(year_data)
        
        results = {
        "expenses_per_type": expenses_per_type,
        "expense_trend": expense_trend,
        "expenses_per_month": expenses_per_month,
        "expenses_per_year": expenses_per_year,
        "expenses_per_month_per_type": expenses_per_month_per_type,
        "expenses_per_year_per_type": expenses_per_year_per_type,
        }
        setData(f"expense_dashboard:{user_id}",results)
        return results

    # gives data for entire dashboard
    @staticmethod
    def dashboard_data(user_id):
        data=getData(f"dashbord_data:{user_id}")
        if data["status"]:return data["data"]
        avg_data=pd.read_sql_query(sql=to_sql_text(dashboard_queries["avg_health_data"].format(user_id=user_id)),con=conn).to_dict("records")[0]
        overall_expense=pd.read_sql_query(to_sql_text(dashboard_queries["overall_expense"].format(user_id=user_id)),con=conn).total_expense.iloc[0]
        df=pd.read_sql_query(sql=to_sql_text(dashboard_queries["reports"].format(user_id=user_id)),con=conn)
        df["report_date"]=df.report_date.astype(str)
        df["submitted_at"]=df.submitted_at.astype(str)
        reports=df.to_dict("records")
        df=pd.read_sql_query(sql=to_sql_text(dashboard_queries["graph_data"].format(user_id=user_id)),con=conn)
        df["submitted_at"]=df.submitted_at.astype(str)
        graph_data=df.to_dict("list")
        resp={"overall_expense":overall_expense,"avg_health_data":avg_data,"reports":reports,"graph_data":graph_data,"appointment":{"id":1,"doctor_name":"Dr Zahir Kazi","date":"6/9/69"}}
        setData(f"dashbord_data:{user_id}",resp)
        return resp



class Doctor:
    @staticmethod
    def getDoctorDashboardData(doctor_id):
        redis_data=getData(f"doctor_dashboard:{doctor_id}")
        if redis_data["status"]:return redis_data["data"]
        df=pd.read_sql_query(to_sql_text("""
        select a.status as appointment_status,a.patient_id,s.status as slot_status,
        s.timing,s.date,s.address_id,service.service_name,service.service_amount from doctor_appointment a
        join doctor_appointmentslot s on a.appointment_slot_id=s.id
        join doctor_doctorservices service on service.id=a.service_id;
        """),con=conn)
        unique_users = df['patient_id'].nunique()

        recurrent_users = df['patient_id'].value_counts()
        recurrent_users_count = recurrent_users[recurrent_users > 1].count()

        appointments_count = len(df)

        patients_per_day = df.groupby('date').size().reset_index(name='appointments')
        patients_per_day["date"]=patients_per_day["date"].astype(str)
        patients_per_day=patients_per_day.to_dict("list")

        unique_patients_per_day = df.groupby('date')['patient_id'].nunique().reset_index(name='unique_patients')
        unique_patients_per_day["date"]=unique_patients_per_day["date"].astype(str)
        unique_patients_per_day=unique_patients_per_day.to_dict("list")

        visited_count = df[df['appointment_status'] == 'VISITED']['patient_id'].nunique()

        not_visited_count = df[df['appointment_status'] == 'NOT VISITED']['patient_id'].nunique()

        appointments_not_visited = df[df['appointment_status'] == 'NOT VISITED'].shape[0]

        unique_users_not_visited = df[df['appointment_status'] == 'NOT VISITED']['patient_id'].nunique()
        df['date'] = pd.to_datetime(df['date']).dt.date  

        # Convert 'timing' column to time format
        df['timing'] = pd.to_datetime(df['timing'], format='%H:%M').dt.time  

        # Get today's date and current time
        today_date = datetime.today().date()
        current_time = datetime.now().time()

        # Filter today's appointments that are yet to happen
        todays_appointments = df[(df['date'] == today_date) & (df['timing'] >= current_time)]

        # Count today's remaining appointments
        todays_appointments_count = todays_appointments.shape[0]

        data= {
            "unique_users":str(unique_users),
            "recurrent_users_count":str(recurrent_users_count),
            "appointments_count":str(appointments_count),
            "patients_per_day":patients_per_day,
            "unique_patients_per_day":unique_patients_per_day,
            "visited_count":str(visited_count),
            "not_visited_count":str(not_visited_count),
            "appointments_not_visited":str(appointments_not_visited),
            "unique_users_not_visited":str(unique_users_not_visited),
            "todays_appointments_count":todays_appointments_count
        }

        setData(f"doctor_dashboard:{doctor_id}",data)
        return data
    
    @staticmethod
    def getDoctorAnalytics(doctor_id):
        redis_data=getData(f"doctor_analytics:{doctor_id}")
        if redis_data["status"]:return redis_data["data"]
        df=pd.read_sql_query(to_sql_text("""
        select a.status as appointment_status,a.patient_id,s.status as slot_status,
        s.timing,s.date,s.address_id, LEFT(da.address, 50) AS address,service.service_name,service.service_amount from doctor_appointment a
        join doctor_appointmentslot s on a.appointment_slot_id=s.id
        join doctor_doctorservices service on service.id=a.service_id
        join doctor_doctoraddress da on s.address_id = da.id
        """),con=conn)

        df['date']=pd.to_datetime(df["date"])

        df['service_amount'] = df['service_amount'].astype(float)

        amount_per_service = df[df['appointment_status'] == 'VISITED'].groupby('service_name')['service_amount'].sum().reset_index(name='amount_generated')
        amount_per_service = amount_per_service.to_dict("list")

        total_amount_generated = df[df['appointment_status'] == 'VISITED']['service_amount'].sum()

        df['month'] = df['date'].dt.to_period('M').astype(str)
        amount_per_month = df[df['appointment_status'] == 'VISITED'].groupby('month')['service_amount'].sum().reset_index(name='amount_generated')
        amount_per_month = amount_per_month.to_dict("list")

        most_used_services = df['service_name'].value_counts().reset_index(name='appointment_count').rename(columns={'index': 'service_name'})
        most_used_services = most_used_services.to_dict("list")

        revenue_per_address = df[df['appointment_status'] == 'VISITED'].groupby('address_id')['service_amount'].sum().reset_index(name='revenue').sort_values(by='revenue', ascending=False)
        revenue_per_address = revenue_per_address.to_dict("list")

        appointments_per_day = df.groupby('date').size().reset_index(name='appointments_booked')
        appointments_per_day['date'] = appointments_per_day['date'].astype(str)  # Convert Timestamp to string
        appointments_per_day = appointments_per_day.to_dict("list")

        appointments_per_month = df.groupby('month').size().reset_index(name='appointments_booked')
        appointments_per_month = appointments_per_month.to_dict("list")

        visited_per_day = df[df['appointment_status'] == 'VISITED'].groupby('date').size().reset_index(name='visited_count')
        visited_per_day['date'] = visited_per_day['date'].astype(str)  # Convert Timestamp to string
        visited_per_day = visited_per_day.to_dict("list")

        not_visited_per_day = df[df['appointment_status'] == 'NOT VISITED'].groupby('date').size().reset_index(name='not_visited_count')
        not_visited_per_day['date'] = not_visited_per_day['date'].astype(str)  # Convert Timestamp to string
        not_visited_per_day = not_visited_per_day.to_dict("list")

        booked_per_day = df[df['slot_status'] == 'BOOKED'].groupby('date').size().reset_index(name='booked_count')
        booked_per_day['date'] = booked_per_day['date'].astype(str)  # Convert Timestamp to string
        booked_per_day = booked_per_day.to_dict("list")

        slots_cancelled_per_day = df[df['slot_status'] == 'CANCELLED'].groupby('date').size().reset_index(name='cancelled_slots')
        slots_cancelled_per_day['date'] = slots_cancelled_per_day['date'].astype(str)  # Convert Timestamp to string
        slots_cancelled_per_day = slots_cancelled_per_day.to_dict("list")

        slots_cancelled_per_month = df[df['slot_status'] == 'CANCELLED'].groupby('month').size().reset_index(name='cancelled_slots')
        slots_cancelled_per_month = slots_cancelled_per_month.to_dict("list")

        data= {
        "amount_per_service": amount_per_service,
        "total_amount_generated": total_amount_generated,
        "amount_per_month": amount_per_month,
        "most_used_services": most_used_services,
        "revenue_per_address": revenue_per_address,
        "appointments_per_day": appointments_per_day,
        "appointments_per_month": appointments_per_month,
        "visited_per_day": visited_per_day,
        "not_visited_per_day": not_visited_per_day,
        "booked_per_day": booked_per_day,
        "slots_cancelled_per_day": slots_cancelled_per_day,
        "slots_cancelled_per_month": slots_cancelled_per_month
        }
        setData(f"doctor_analytics:{doctor_id}",data)
        return data


    # @staticmethod
    # def getPatientsWithAccess(user_id):
    #     df=pd.read_sql_query(
    #         sql=to_sql_text(
    #             f'''
    #             select patient_id,concat(p.first_name,p.last_name) as name,requested_at::timestamp::text
    #             from doctor_requestaccess d join authentication_customuser p
    #             on p.id=d.patient_id
    #             where doctor_id={user_id};
    #             '''
    #             ),con=conn)
    #     return df.to_dict("records")
