import requests
import streamlit as st
import pandas as pd
import json

st.title('🤖 Machine Learning App')

st.info('This is app builds a machine learning model!')

# Define the period parameter for DHIS2 API (you can assign this dynamically as needed)
period = '2023Q1'  # Example period, change this based on your requirement

# DHIS2 API URL with the period variable
dhis2_url = f"https://centraldhis.mohfw.gov.bd/dhismohfw/api/dataValueSets.json?orgUnitIdScheme=code&dataSet=BPJNays7ZoS&orgUnit=dNLjKwsVjod&children=true&period={period}"

# Set the username and password for DHIS2 basic authentication
dhis2_username = 'ipasbangladesh'
dhis2_password = 'Ipas@2020'

# Send the GET request to the DHIS2 API
dhis2_response = requests.get(dhis2_url, auth=(dhis2_username, dhis2_password))

# Check if the request to DHIS2 was successful
if dhis2_response.status_code == 200:
    dhis2_output = dhis2_response.text
    # Clean the output string
    dhis2_output = dhis2_output.replace(f'{{"dataSet":"BPJNays7ZoS","period":"{period}","orgUnit":"10000000","dataValues":', '')
    dhis2_output = dhis2_output + "BANGLADESH"
    dhis2_output = dhis2_output.replace('}BANGLADESH', '')

    # Validate the output
    if dhis2_output.find("dataElement") == -1:
        print("Invalid DataElement in the JSON format found!")
    elif len(dhis2_output) < 100:
        print(f"Data not available to import for the period {period}")
    else:
        # Convert the cleaned output to JSON
        dhis2_data = json.loads(dhis2_output)

        # Extract and convert 'dataValues' to a DataFrame
        if 'dataValues' in dhis2_data:
            dhis2_df = pd.DataFrame(dhis2_data['dataValues'])
            print("DHIS2 DataFrame:")
            print(dhis2_df.head())  # Display the first few rows of the DataFrame
        else:
            print("No 'dataValues' found in the DHIS2 response.")
else:
    print(f"Failed to retrieve data from DHIS2. Status code: {dhis2_response.status_code}")


# HRM API URL for facilities data
# hrm_url = "https://hrm.dghs.gov.bd/api/1.0/facilities/get?facilitytype_id=[2,5,19,24,25,26,27,28,29]&limit=1000"

# # Define headers with the authentication token for HRM API
# hrm_headers = {
#     'X-Auth-Token': '77223156d66e58f8591b2cc247f493ccf5ebb9d12b2c4bde6a4ddaebaad7045c',
#     'client-id': '185924'
# }

# # Send a GET request to the HRM API
# hrm_response = requests.get(hrm_url, headers=hrm_headers)

# # Check if the request to HRM was successful
# if hrm_response.status_code == 200:
#     hrm_data = hrm_response.json()

#     # Convert the data to a Pandas DataFrame (assuming the 'data' key contains the list of facilities)
#     hrm_df = pd.DataFrame(hrm_data['data'])
    
#     print("HRM DataFrame:")
#     print(hrm_df.head())  # Display the first few rows of the HRM DataFrame
# else:
#     print(f"Failed to retrieve data from HRM. Status code: {hrm_response.status_code}")
# st.write("HRM")


dhis2_df

