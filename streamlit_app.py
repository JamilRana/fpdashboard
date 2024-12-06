import requests
import pandas as pd

# Define the API URL
url = "https://hrm.dghs.gov.bd/api/1.0/facilities/get?facilitytype_id=[2,5,19,24,25,26,27,28,29]&limit=1000"

# Define headers with the authentication token
headers = {
    'X-Auth-Token': '77223156d66e58f8591b2cc247f493ccf5ebb9d12b2c4bde6a4ddaebaad7045c',
    'client-id': '185924'
}

# Send a GET request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Get the JSON response from the API
    data = response.json()
    
    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data['data'])  # Assuming the JSON structure has a key 'data' that contains the list of facilities
    
    # Display the first few rows of the dataframe
    print(df.head())
else:
    print("Failed to retrieve data. Status code:", response.status_code)
