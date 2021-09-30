#! usr/bin/env python3
import json
import requests


def coinHistory():

    # api-endpoint 
    # https://www.coingecko.com/en/api#explore-api
    url = 'https://api.coingecko.com/api/v3/coins/donut?market_data=true'

    response = requests.get(url)

    if response.status_code == 200:
        coinJSON = response.json()

        supply = coinJSON['market_data']['total_supply']

    else:
        supply = "ERROR"   


    return supply
