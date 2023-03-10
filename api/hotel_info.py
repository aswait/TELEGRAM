from api.api_request import api_request
from telebot.types import InputMedia
from typing import List
import json


def hotel_info(hotels: List[dict], photos: int = None) -> List[dict]:
    hotels_info = list()
    for hotel in hotels:
        payload = {
            'currency': 'USD',
            'eapid': 1,
            'locale': 'ru_RU',
            'siteId': 300000001,
            'propertyId': hotel['hotel_id']
        }

        response = api_request('properties/v2/detail', payload, 'POST')
        response = json.loads(response)['data']['propertyInfo']
        hotel_information = dict()
        hotel_information['name']: str = response['summary']['name']     # Название отеля
        hotel_information['address']: str = response['summary']['location']['address']['addressLine']    # Адрес отеля

        hotel_information['distance']: float = hotel['distance']
        hotel_information['url']: str = f'https://www.hotels.com/h{hotel["hotel_id"]}.Hotel-Information'

        coordinates = response['summary']['location']['coordinates']
        hotel_information['map']: str = f"https://maps.google.com/maps?z=12&t=m&q=loc:" \
                                        f"{coordinates['latitude']},{coordinates['longitude']}"

        hotel_information['price']: float = round(hotel['hotel_price'], 2)

        rating = response['summary']['overview']['propertyRating']
        if rating:
            hotel_information['rating'] = rating['rating']
        else:
            hotel_information['rating'] = 'Нет данных'

        review = response['reviewInfo']['summary']['overallScoreWithDescriptionA11y']['value']
        if review:
            hotel_information['review'] = review
        else:
            hotel_information['review'] = 'Нет данных'

        hotels_info.append(hotel_information)

        if photos:
            images = list()
            photo = response['propertyGallery']['images']
            for i_image in range(photos):
                image = InputMedia(type='photo', media=photo[i_image]['image']['url'])

                images.append(image)

            hotel_information['images'] = images

    return hotels_info
