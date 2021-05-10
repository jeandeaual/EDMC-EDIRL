import logging
import requests
from typing import Optional
from urllib.parse import urljoin

WIKIPEDIA_URL = 'https://en.wikipedia.org/'


def get_wikipedia_url(name: str) -> str:
    return urljoin(WIKIPEDIA_URL, f'wiki/{name}')


def query_wikipedia_page(name: str) -> Optional[str]:
    url = get_wikipedia_url(name)

    response = requests.get(url)
    if response.history:
        logging.debug("request was redirected")
        last_response = response.history[-1]
        logging.debug(f'got redirected to {last_response.url} with response code {last_responsetus_code}')
        # TODO: Check if we got redirected to index.php
        return None
    else:
        logging.debug("request was not redirected")
        return url


query_wikipedia_page('Test')
