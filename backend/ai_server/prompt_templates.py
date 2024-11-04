EXPENSE_PROMPT='''
 You are a medical entity recognition system. Your task is to extract information and return a JSON object with exactly three keys: "amount", "expenditure", and "status". 

1. Extract the monetary value and assign it to the "amount" key and value should be whole number.
2. Identify the category of expenditure and assign it to the "expenditure" key. The expenditure should be classified into one of the following categories: "tests", "doctor", or "medicine".
3. If the input is related to medical expenses, set the "status" key to "true". If the input is unrelated or outside your scope, set the "status" key to "false".

Ensure the output is a simple JSON object with no additional text or nested structures.
give me the json with no preamble and the value of status key will be in double quotes cumpolsurily.
'''

prompts={
    "type_prompt":'''
you are a medical report classifier.
you will be given a medical report in text and you have to classify it in blood_report or other.
if there are values of hemoglobin,rbc count wbc count,platelet count bilirubin etc then it is a blood report else other.
Give me the result in Json format with key as "type" with no preamble and no nested json.
''',
    'blood_prompt':'''
you are a medical report parser.
Give me the output in json format strictly with no preamble.
If you dont get any value assign it None
Extract the following fields
    name of the doctor with key as "doctor_name"
    date of report with key as "date_of_report" with dd/mm/yy format with no leading zeroes
    date of collection with key as "date_of_collection" with dd/mm/yy format with no leading zeroes
    hemoglobin with key as "hemoglobin"
    rbc count with key as "rbc_count"
    wbc count with key as "wbc_count"
    pcv with key as "pcv"
    iron with key as "iron"
    sodium with key "sodium"
    pottasium with key "potassium"
    phosphorus with key "phosphorus"
    chloride with key "chloride"
    platelet count with key as "platelet_count"
    bilirubin total with key as "bilirubin_total"
    bilirubin direct with key as "bilirubin_direct"
    bilirubin indirect with key as "bilirubin_indirect"
    proteins with key as "proteins"
    calcium with key as "calcium"
    albumin with key as "albumin"
    Globulin with key as "globulin"
    Blood Urea with the key "blood_urea"
    Blood Urea Nitrogen with the key "blood_urea_nitrogen"
    S. Creatinine with the key "s_creatinine"
    S. Uric Acid with the key "s_uric_acid"
    S. Phosphorus with the key "s_phosphorus"
    Neutrophils with the key "neutrophils".
    Lymphocytes with the key "lymphocytes".
    Sr. Cholesterol with the key "sr_cholesterol".
    HDL Cholesterol with the key "hdl_cholesterol".
    fasting sugar with key "fasting_sugar"
    after lunch sugar with key "after_lunch_sugar"
Summarize the medical report, focusing on any values that are abnormal or outside the normal range with key "summary"
Strictly give me in proper json format with no nested json and  with no preamble.
''' ,
    "other_prompt":'''
you are a medical report summarizer and entity extractor.
Give me the following details in json format
    name of the doctor with key as "doctor_name"
    date of report with key as "date_of_report" with dd/mm/yy format with no leading zeroes
    date of collection with key as "date_of_collections" with dd/mm/yy format with no leading zeroes
    summary the report with key as "summary".
Only give me json with no preamble
''',
"health_summary_prompt":'''
  You will receive a user's complete medical history, including:

Date of report
Type of report
Detailed report data with various metrics, each indicating its normal range, unit, and current measured value.
Task: Analyze this data to:

Provide an overall health summary of approximately 400 words that:

Highlights trends in critical health metrics and any notable fluctuations over time.
Identifies deficiencies, excesses, or patterns that may indicate potential health concerns 
Assesses the user's overall health status, detailing how well their results align with healthy ranges and discussing implications of any recurring deviations from these ranges.
Create a personalized diet and nutrition plan that:

Recommends specific foods and dietary adjustments to address the user's unique needs (e.g., foods rich in iron, vitamin D, or low in sodium).
Includes general advice to support balanced nutrition and ongoing health improvement based on observed trends.
Output Format: Return a JSON object structured as follows, with no extra text or preamble:

"summary": A string containing the detailed health summary.
"plans": A string containing the personalized diet and nutrition plan.
Return the JSON in a precise format with no additional whitespace before or after keys and no preamble.
'''
}

data_template={
  "hemoglobin": {
    "value": -1,
    "min": 12.1,
    "max": 15.5,
    "unit": "g/dL"
  },
  "rbc_count": {
    "value": -1,
    "min": 4.2,
    "max": 5.4,
    "unit": "million cells/μL"
  },
  "wbc_count": {
    "value": -1,
    "min": 4.5,
    "max": 11.0,
    "unit": "thousand cells/μL"
  },
  "pcv": {
    "value": -1,
    "min": 36,
    "max": 50,
    "unit": "%"
  },
  "iron": {
    "value": -1,
    "min": 60,
    "max": 170,
    "unit": "μg/dL"
  },
  "sodium": {
    "value": -1,
    "min": 135,
    "max": 145,
    "unit": "mmol/L"
  },
  "potassium": {
    "value": -1,
    "min": 3.5,
    "max": 5.0,
    "unit": "mmol/L"
  },
  "phosphorus": {
    "value": -1,
    "min": 2.5,
    "max": 4.5,
    "unit": "mg/dL"
  },
  "chloride": {
    "value": -1,
    "min": 98,
    "max": 107,
    "unit": "mmol/L"
  },
  "platelet_count": {
    "value": -1,
    "min": 150000,
    "max": 450000,
    "unit": "cells/μL"
  },
  "bilirubin_total": {
    "value": -1,
    "min": 0.1,
    "max": 1.2,
    "unit": "mg/dL"
  },
  "bilirubin_direct": {
    "value": -1,
    "min": 0.0,
    "max": 0.3,
    "unit": "mg/dL"
  },
  "bilirubin_indirect": {
    "value": -1,
    "min": 0.1,
    "max": 0.8,
    "unit": "mg/dL"
  },
  "proteins": {
    "value": -1,
    "min": 6.0,
    "max": 8.0,
    "unit": "g/dL"
  },
  "calcium": {
    "value": -1,
    "min": 8.5,
    "max": 10.2,
    "unit": "mg/dL"
  },
  "albumin": {
    "value": -1,
    "min": 3.5,
    "max": 5.0,
    "unit": "g/dL"
  },
  "globulin": {
    "value": -1,
    "min": 2.0,
    "max": 4.0,
    "unit": "g/dL"
  },
  "blood_urea": {
    "value": -1,
    "min": 7,
    "max": 20,
    "unit": "mg/dL"
  },
  "blood_urea_nitrogen": {
    "value": -1,
    "min": 7,
    "max": 20,
    "unit": "mg/dL"
  },
  "s_creatinine": {
    "value": -1,
    "min": 0.6,
    "max": 1.2,
    "unit": "mg/dL"
  },
  "s_uric_acid": {
    "value": -1,
    "min": 3.5,
    "max": 7.2,
    "unit": "mg/dL"
  },
  "s_phosphorus": {
    "value": -1,
    "min": 2.5,
    "max": 4.5,
    "unit": "mg/dL"
  },
  "neutrophils": {
    "value": -1,
    "min": 40,
    "max": 75,
    "unit": "%"
  },
  "lymphocytes": {
    "value": -1,
    "min": 20,
    "max": 45,
    "unit": "%"
  },
  "sr_cholesterol": {
    "value": -1,
    "min": 0,
    "max": 200,
    "unit": "mg/dL"
  },
  "hdl_cholesterol": {
    "value": -1,
    "min": 40,
    "max": 60,
    "unit": "mg/dL"
  },
  "fasting_sugar": {
    "value": -1,
    "min": 70,
    "max": 100,
    "unit": "mg/dL"
  },
  "after_lunch_sugar": {
    "value": -1,
    "min": 70,
    "max": 140,
    "unit": "mg/dL"
  }
}
