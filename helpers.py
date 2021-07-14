import requests
import logging

logging.basicConfig(level=logging.INFO)

def test_status_code(r):
    if r.status_code != 200:
        logging.warning(f"Error: Request was not successful. It returned status code {r.status_code}")
        exit()
