

import pandas as pd
import requests # type: ignore

def fetch_data_from_api():
    # API endpoint to fetch
    api_url = '#YOUR_API_ENDPOINT_HERE#'
    # Fetch data from the API
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Convert API response to DataFrame
        api_data = response.json()
        df = pd.DataFrame(api_data)

        # Return the data as a dictionary
        return df.to_dict(orient='list')
    
    else:
        print(f"Failed : {response.status_code}")
        return None