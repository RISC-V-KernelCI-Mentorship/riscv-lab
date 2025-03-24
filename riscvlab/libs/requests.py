import requests
from requests.adapters import HTTPAdapter, Retry

def create_session(base_url):
    s = requests.Session()
    retries = Retry(total=3,
                    backoff_factor=0.1,
                    status_forcelist=[429, 500, 502, 503, 504, 507])
    s.mount(base_url, HTTPAdapter(max_retries=retries))
    return s

