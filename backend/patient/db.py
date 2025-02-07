import psycopg2,json,os
import pandas as pd
from sqlalchemy import create_engine,text as to_sql_text
from utils import getData,setData


DB_NAME=os.environ["DB_NAME"]
USER=os.environ["USER"]
PASSWORD=os.environ["PASSWORD"]
DB_HOST=os.environ["DB_HOST"]

connection_string = f'postgresql+psycopg2://{USER}:{PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
engine = create_engine(connection_string)
conn=engine.connect()

queries=json.load(open("queries.json"))
dashboard_queries=json.load(open("dashboard_queries.json"))

# provides data for health check dashboard
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
