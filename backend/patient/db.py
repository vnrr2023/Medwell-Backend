import psycopg2
import pandas as pd
from sqlalchemy import create_engine


db_username = 'myuser'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'medwell_db'

connection_string = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

def connect_db():
    connection = psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='medwell_db' ,
        user='myuser' ,
        password='root' 
    )
    return connection,connection.cursor()

queries={
    'health_check':'''
    select submitted_at,hemoglobin,rbc_count,wbc_count,platelet_count,pcv,bilirubin,proteins, calcium,blood_urea,sr_cholestrol
    from patient_report pr join patient_reportdetail rd
    on pr.id=rd.report_id
    where user_id={user_id};
    ''',
    'average_query':'''
    SELECT 
        AVG(CASE WHEN hemoglobin <> '-1' THEN CAST(hemoglobin AS FLOAT) END) AS avg_hemoglobin,
        AVG(CASE WHEN rbc_count <> '-1' THEN CAST(rbc_count AS FLOAT) END) AS avg_rbc_count,
        AVG(CASE WHEN wbc_count <> '-1' THEN CAST(wbc_count AS FLOAT) END) AS avg_wbc_count,
        AVG(CASE WHEN platelet_count <> '-1' THEN CAST(platelet_count AS FLOAT) END) AS avg_platelet_count,
        AVG(CASE WHEN pcv <> '-1' THEN CAST(pcv AS FLOAT) END) AS avg_pcv,
        AVG(CASE WHEN bilirubin <> '-1' THEN CAST(bilirubin AS FLOAT) END) AS avg_bilirubin,
        AVG(CASE WHEN proteins <> '-1' THEN CAST(proteins AS FLOAT) END) AS avg_proteins,
        AVG(CASE WHEN calcium <> '-1' THEN CAST(calcium AS FLOAT) END) AS avg_calcium,
        AVG(CASE WHEN blood_urea <> '-1' THEN CAST(blood_urea AS FLOAT) END) AS avg_blood_urea,
        AVG(CASE WHEN sr_cholestrol <> '-1' THEN CAST(sr_cholestrol AS FLOAT) END) AS avg_sr_cholestrol
    FROM 
        patient_report pr 
    JOIN 
        patient_reportdetail rd ON pr.id = rd.report_id
    WHERE 
        user_id = {user_id};
    ''',
    'report_count_query': '''select count(*) as num_reports from patient_report where user_id={user_id}; ''',
    "overall_expense":'''SELECT SUM(CAST(amount AS DECIMAL)) as total_expense from patient_expense where user_id={user_id} ;''',
    "recent_expenses":'''select expense_type,amount,date(date) from patient_expense where user_id={user_id} order by date desc limit 10;''',
    "expense_per_type":'''
    SELECT expense_type,SUM(CAST(amount AS DECIMAL)) as total
    from patient_expense
    where user_id={user_id}
    group by expense_type
    ;
    ''',
    "expense_trend":'''
    SELECT CAST(amount AS DECIMAL) as expenses
    from patient_expense
    where user_id={user_id}
    ;
    ''',
    "expenses_per_month":'''
    SELECT to_char(date, 'Month') AS month_name,sum(CAST(amount AS DECIMAL)) as expenses,date_part('month', date) AS month
    from patient_expense
    where user_id={user_id}
    group by to_char(date, 'Month'),date_part('month', date)
    order by date_part('month', date)
    ;
    ''',
    "expenses_per_year":'''
    SELECT sum(CAST(amount AS DECIMAL)) as expenses,date_part('year', date) AS year
    from patient_expense
    where user_id={user_id}
    group by date_part('year', date)
    order by date_part('year', date)
    ;
    ''',
    "expense_per_month_per_type":'''
    SELECT date_part('month', date) AS month,expense_type,sum(CAST(amount AS DECIMAL)) as expenses
    from patient_expense
    where user_id={user_id}
    group by date_part('month', date),expense_type
    order by date_part('month', date)
    ;    
    ''',
    "expenses_per_year_per_type":'''
    SELECT date_part('year', date) AS year,expense_type,sum(CAST(amount AS DECIMAL)) as expenses
    from patient_expense
    where user_id={user_id}
    group by date_part('year', date),expense_type
    order by date_part('year', date)
    ;
    '''


}


def provide_health_check_data(user_id):
    count=pd.read_sql_query(queries['report_count_query'].format(user_id=user_id),engine)['num_reports'][0]
    if count<=3:
        return {"status":False,"count":count}
    df=pd.read_sql_query(queries['health_check'].format(user_id=user_id),engine)
    df.replace("-1",None,inplace=True)
    df['submitted_at'] = df['submitted_at'].astype(str)
    data=df.to_dict("list")
    avg_data=pd.read_sql_query(queries['average_query'].format(user_id=user_id),engine).to_dict("records")[0]
    return {"status":True,"data":data,"avg_data":avg_data}


def provide_expense_data(user_id):
    conn,cursor=connect_db()
    cursor.execute(queries["overall_expense"].format(user_id=user_id))
    overall_expense=str(cursor.fetchone()[0])
    df=pd.read_sql_query(queries["recent_expenses"].format(user_id=user_id),engine)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    data=df.to_dict("records")
    return {"overall_expense":overall_expense,"expenses":data}
    

def provide_expense_dashboard(user_id):
    df=pd.read_sql_query(queries["expense_per_type"].format(user_id=user_id),engine)
    expenses_per_type=df.to_dict("list")
    df=pd.read_sql_query(queries["expense_trend"].format(user_id=user_id),engine)
    expense_trend=df.to_dict("list")
    df=pd.read_sql_query(queries["expenses_per_month"].format(user_id=user_id),engine)[["month_name","expenses"]]
    expenses_per_month=df.to_dict("list")
    df=pd.read_sql_query(queries["expenses_per_year"].format(user_id=user_id),engine)[["year","expenses"]]
    expenses_per_year=df.to_dict("list")
    df=pd.read_sql_query(queries["expense_per_month_per_type"].format(user_id=user_id),engine)
    grouped_df = df.groupby(by="month")
    expenses_per_month_per_type=[]
    for month,df in grouped_df:
        month_data = {
            "month": month,
            "data": df[["expense_type","expenses"]].to_dict("list")
        }
        expenses_per_month_per_type.append(month_data)
    df=pd.read_sql_query(queries["expenses_per_year_per_type"].format(user_id=user_id),engine)
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
    return results