
import os
import requests
from flight_data_W_D39_v00_r18 import FlightData

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/v2"
TEQUILA_API_KEY = os.environ.get('TEQUILA_API_KEY', 'Key does not exist')


class FlightSearch:
    # this class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.city_name = None
        self.price = None

    def get_destination_code(self, city_name):
        self.city_name = city_name
        # self.price = price
        # GET request from Tequila API

        headers = {
            "apikey": TEQUILA_API_KEY
            }

        # city_name="City_name test: PRG"

        query_params = {
            "term":city_name,
            "locale":"en-US",
            "location_types":"airport",
            "limit":7,
            "active_only":"true",
        }
        # iata_code = flight_search.get_destination_code(row["city"])
        query_request_url = "https://api.tequila.kiwi.com/locations/query"      #  toss this: f"{TEQUILA_ENDPOINT}/locations/query"
        query_response = requests.get(url=query_request_url, headers=headers, params=query_params)

        query_response.raise_for_status()
        query_data = query_response.json()
        # print(f"The query_data is: {query_data}")

        for city_iteration in range(query_params['limit']):
            # global IATA_city_code
            IATA_city_code = query_data['locations'][city_iteration]['code']

            # return "TESTING" code for now, to ensure it's working. We can get Tequila API data later:
            dest_code = IATA_city_code   #entered into IATA Code column of that particular row's city name
            print(f"The city name is: {city_name}")
            print(dest_code)
            return dest_code

   ######################## END OF IATA CODE LOGIC ########################


    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):

        # TODO: price_and_city_params taken to main.py

        # Include your API key in the headers
        price_and_city_headers = {
            "apikey": TEQUILA_API_KEY  # Replace YOUR_API_KEY_HERE with your actual Tequila API key
        }


        # the query:
        price_and_city_search_params_query = {
            "fly_from": origin_city_code,  # SAN
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"), # nothing needed to import for this function to kick in
            "date_to": to_time.strftime("%d/%m/%Y"),
            # "return_from": "04/04/2023",
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 28,
            # "max_fly_duration": 20,
            # "ret_from_diff_city": "true",
            # "ret_to_diff_city": "true",
            "one_for_city": 1,  # Only 1 response for each city chosen
            # "one_per_date": 0,
            # "adults": 1,
            # "children": 0,
            # "infants": 0,
            # "selected_cabins": "C",
            # "mix_with_cabins": "M",
            # "adult_hold_bag": "1,0",
            # "adult_hand_bag": "1,1",
            # "child_hold_bag": "0,0",
            # "child_hand_bag": "0,0",
            # "only_working_days": "false",
            # "only_weekends": "false",
            # "partner_market": "us",
            # "price_from": 0,
            # "price_to": 550,    # OPTIONAL for PRICE Limit
            "curr": "USD",
            "max_stopovers": 2,
            # "max_sector_stopovers": 2,
            # "vehicle_type": "aircraft",
            # "sort": "price",
            "limit": 1  # OPTIONAL: to get the top/cheapest flight of the whole bunch that were found in the search
        }

        # flight_search.get_price(price_and_city_params)

    # else:
    # # if "iatacode" is not empty, print a message and skip to the next row:
    # print(f"iataCode for {row['city']} is already set to {row['iataCode']}, Skipping this row...")

    # define the endpoint Price and City search URL:
        price_and_city_url = "https://api.tequila.kiwi.com/v2/search"

        # Make the GET request
        price_and_city_response = requests.get(url=price_and_city_url, params=price_and_city_search_params_query,
                                               headers=price_and_city_headers)
        # print(f"The price_and_city_response is: {price_and_city_response}")

        price_and_city_response.raise_for_status()
        price_and_city_data = price_and_city_response.json()
        # print(f"The price_and_city_data is: {price_and_city_data}")

        # TODO: Print the City and Price for all the cities listed:

        # attempting to check data inside response:
        try:
            data = price_and_city_response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")   # or {city_name}
            return None
        # try:
        #     data = response.json()["data"][0]
        # except IndexError:
        #     print(f"No flights found for {destination_city_code}.")
        #     return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: ${flight_data.price}")   # in US Dollars, currency. not British pounds £
        return flight_data


        # if 'data' in price_and_city_data and price_and_city_data['data']:
        #     self.price = price_and_city_data['data'][0]['price']
        #     print(f"The cheapest flight price is: {self.price}")
        #     return self.price
        # else:
        #     print("No flight data was found.")
        #     return None
