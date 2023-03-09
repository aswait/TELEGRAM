import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, TooManyRedirects, RequestException
from config_data import config
from utils.logging import logger, log_api_request


@log_api_request
def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type,  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # В зависимости от типа запроса вызываем соответствующую функцию
    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            url=url,
            payload=params,
        )


def get_request(url, params):
    try:
        response = requests.get(
            url,
            headers={"X-RapidAPI-Key": config.RAPID_API_KEY, "X-RapidAPI-Host": config.RAPID_API_HOST},
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.text
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout, RequestException) as exc:
        logger.exception(exc)


def post_request(url, payload):
    try:
        response = requests.post(
            url,
            headers={"X-RapidAPI-Key": config.RAPID_API_KEY, "X-RapidAPI-Host": config.RAPID_API_HOST},
            json=payload,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.text
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout, RequestException) as exc:
        logger.exception(exc)
