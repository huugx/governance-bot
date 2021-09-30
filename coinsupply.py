#! usr/bin/env python3
import json
import requests


def coinHistory():

    # api-endpoint 
    # https://www.coingecko.com/en/api#explore-api
    coinJSON = 'https://api.coingecko.com/api/v3/coins/donut?market_data=true'

    coinJSON = requests.get(url = coinJSON)
    coinJSON = coinJSON.json()

    supply = coinJSON['market_data']['total_supply']


    return supply