import requests
import pandas as pd
import json
import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.title('🤖 Machine Learning App')

st.info('This is app builds a machine learning model!')

# Fetch facility data
facility_url = "https://hrm.dghs.gov.bd/api/1.0/facilities?facilitytype_id=[2,5,19,24,25,26,27,28,29]&rows_per_page=1000"

# Headers with authentication token
headers = {
    'X-Auth-Token': '77223156d66e58f8591b2cc247f493ccf5ebb9d12b2c4bde6a4ddaebaad7045c',
    'client-id': '185924'
}

# Send request to facility API
facility_response = requests.get(facility_url, headers=headers)
if facility_response.status_code == 200:
    facility_data = json.loads(facility_response.text)
    if 'data' in facility_data and 'items' in facility_data['data']:
        facility_df = pd.DataFrame(facility_data['data']['items'])
        facility_df = facility_df[['code', 'name', 'division_name', 'district_name', 'upazila_name', 'latitude', 'longitude', 'email_1','facility_type_name']]
    else:
        print("Key 'items' not found in 'data'.")
        facility_df = pd.DataFrame()
else:
    print(f"Facility API request failed with status code {facility_response.status_code}")
    facility_df = pd.DataFrame()

# Fetch dataValues
period = "202209"
data_url = f"https://centraldhis.mohfw.gov.bd/dhismohfw/api/dataValueSets.json?orgUnitIdScheme=code&dataSet=eiFwqClSR1L&orgUnit=dNLjKwsVjod&children=true&period={period}"

username = "ipasbangladesh"
password = "Ipas@2020"

data_response = requests.get(data_url, auth=(username, password))
if data_response.status_code == 200:
    try:
        data_values = json.loads(data_response.text)
        if "dataValues" in data_values:
            df = pd.DataFrame(data_values["dataValues"])
            if "storedBy" in df.columns:
                service_df = df.rename(columns={'orgUnit': 'code'})
            else:
                print("'storedBy' column not found in dataValues.")
                service_df = pd.DataFrame()
        else:
            print("Key 'dataValues' not found in response.")
            service_df = pd.DataFrame()
    except json.JSONDecodeError as e:
        print("Failed to decode JSON from dataValues response.", e)
        service_df = pd.DataFrame()
else:
    print(f"DataValues API request failed with status code {data_response.status_code}")
    service_df = pd.DataFrame()

if not service_df.empty and not facility_df.empty:
    merge_df = pd.merge(service_df, facility_df, on='code', how='left')
else:
    print("Merge operation skipped due to empty DataFrames.")

service_name_df = pd.DataFrame({
    'dataElement': ['K57gUnDQnwm', 'x0cbbGvBn0S','or4yszH6rk3','rBAkiNGXSzQ','LWO7tZy3ViW',
                    'jfdK2sC7Lqp','zNBrRg864z7','qiTMg2vrKb5','Sdr0eXythRZ','I09GY3HKJQR',
                    'nVKUShBPnzx','x52YO9hnkDR','gpDhIDxvcvu','DoIvZ0ZmNbM','Gszz2rlnhiB',
                    'aDen6QpghPD','waqvAoc4WSR','K4lZTJcE5Lk','vx2EjeajAGy','DxAcF554FGc',
                    'fWmUtJxspDt','fxMp4OAoB6P','oUFlfqHT9jK','pUNL9DfYe0M','seXU9pm1aGE',
                    'SCCzP27AkTQ','FfkJopJ0ziu',
                    'KcHucnkMQjy', 'Zw8XL8v5RG3', 'bdRdqXa4zi4'],
    'category': ['Oral Pill','Oral Pill','Oral Pill','Oral Pill','Oral Pill',
                 'Condom','Condom','Condom','Condom','Condom',
                 'Injectable','Injectable','Injectable','Injectable','Injectable',
                 'IUD','IUD','IUD','IUD','IUD',
                 'Implant','Implant','Implant','Implant','Implant',
                 'Vasectomy','Vasectomy',
                 'Tubectomy','Tubectomy','Tubectomy'],
    'sub_category':['oral pills users – old','oral pills users – new','FP Oral Pill PPFP Old','FP Oral Pill PPFP New','FP Oral Pill PAFP Total',
                    'Condom users – old','Condom users – new','FP Condom PPFP Old','FP Condom PPFP New','FP Condom PAFP Total',
                    'Injectable users – old','Injectable users - new','FP Injectable PPFP Old','FP Injectable PPFP New','FP Injectable PAFP Total',
                    'IUD users – old','IUD users – new','FP IUD PPFP Old','FP IUD PPFP New','FP IUD PAFP Total',
                    'Implant users – old','Implant users – new','FP Implant PPFP Old','FP Implant PPFP New','FP Implant PAFP Total',
                    'FP NSV Interval Total','FP NSV PPFP Total',
                    'FP Tubectomy Interval Total','FP Tubectomy PPFP Total','FP Tubectomy PAFP Total'],
    'client_type': ['Interval Client','Interval Client', 'Post-partum Client','Post-partum Client', 'Post-abortion Client',
                    'Interval Client','Interval Client', 'Post-partum Client','Post-partum Client', 'Post-abortion Client',
                    'Interval Client','Interval Client', 'Post-partum Client','Post-partum Client', 'Post-abortion Client',
                    'Interval Client','Interval Client', 'Post-partum Client','Post-partum Client', 'Post-abortion Client',
                    'Interval Client','Interval Client', 'Post-partum Client','Post-partum Client', 'Post-abortion Client',
                    'Interval Client', 'Post-partum Client',
                    'Interval Client', 'Post-partum Client','Post-abortion Client'],
    'method_type': ['Short Acting Method','Short Acting Method','Short Acting Method','Short Acting Method','Short Acting Method',
                    'Short Acting Method','Short Acting Method','Short Acting Method','Short Acting Method','Short Acting Method',
                    'Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method',
                    'Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method',
                    'Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method','Long Acting Reversible Contraseptive Method',
                    'Permanent Method','Permanent Method',
                    'Permanent Method','Permanent Method','Permanent Method'],
})

merge2_df = pd.merge(merge_df, service_name_df, on='dataElement', how='left')

print(merge2_df[['dataElement','category','value']])
merge2_df['value'] = pd.to_numeric(merge2_df['value'], errors='coerce')

grouped_sum = merge2_df.groupby(['category','division_name','facility_type_name'])['value'].sum().reset_index()
grouped_sum

grouped_sum = merge2_df.groupby(['name','division_name'])['value'].sum().reset_index()
print(grouped_sum)
