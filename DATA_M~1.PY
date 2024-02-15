import requests
import json, pprint, os

SHEETY_PRICES_URL_ENDPOINT = "https://api.sheety.co/def1d491a308d71f282a58a606026fea/sirisFlightDeals/prices"

#This class is responsible for talking to the Google Sheet.
class DataManager:
    # def __init__(self, JSON_data_in_PyDict_format):
    def __init__(self):
        self.destination_data = {}
        self.sheety_endpoint = os.environ.get('SHEETY_UPDATE_ENDPOINT', 'No endpoint found')
        self.bearer_token = os.environ.get('SHEETY_BEARER_TOKEN', 'Bearer Token not found')

    def get_request_for_getting_destination_data(self):
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        sheety_API_GET_response = requests.get(url=SHEETY_PRICES_URL_ENDPOINT, headers=headers)
        sheety_API_GET_response.raise_for_status()  # this will raise an error for bad responses
        data = sheety_API_GET_response.json()
        print(f"JSON format of the current Google sheet: {json.dumps(data, indent=4)}")  # this will print the formatted JSON response
        self.destination_data = data.get("prices", [])  # use .get to avoid KeyError and provide a default value
        return self.destination_data


    def update_destination_codes(self, sheet_data):   # remove: def destination_data(self): already used
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        for city in self.destination_data:   #remove () after destination_data
            if city["iataCode"]:
                put_url = f"{self.sheety_endpoint}/{city['id']}"
                new_data = {
                    "price": {     # singular form of the prices sheet name
                        "iataCode": city["iataCode"]
                    }
                }
                response = requests.put(put_url, json=new_data, headers=headers)
                print(response.text)
                response.raise_for_status()
