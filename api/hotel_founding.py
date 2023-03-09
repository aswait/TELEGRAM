from api.api_request import api_request
from datetime import date
from typing import Any, List
import json


def hotel_founding(location_id: str, check_in: date, check_out: date,
                   hotels_amount: int, sort: str, req_filter: Any) -> List[dict]:
    payload = {'currency': 'USD',
               'eapid': 1,
               'locale': 'ru_RU',
               'siteId': 300000001,
               'destination': {
                  'regionId': location_id
               },
               'checkInDate': {
                  'day': check_in.day,
                  'month': check_in.month,
                  'year': check_in.year
               },
               'checkOutDate': {
                  'day': check_out.day,
                  'month': check_out.month,
                  'year': check_out.year
               },
               'rooms': [{'adults': 1}],
               'resultsStartingIndex': 0,
               'resultsSize': hotels_amount,
               'sort': sort,
               'filters': req_filter}

    response = api_request('properties/v2/list', payload, 'POST')
    response = json.loads(response)
    hotels_list = list()

    if response:
        for hotel in response['data']['propertySearch']['properties']:
            data = dict()
            data['hotel_id'] = hotel.get('id')
            data['hotel_price'] = hotel['price']['lead']['amount']

            distance = round(hotel['destinationInfo']['distanceFromDestination']['value'] * 1.60934, 2)
            data['distance'] = distance
            hotels_list.append(data)

        return hotels_list
