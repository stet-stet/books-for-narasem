import requests
from bs4 import BeautifulSoup
import bfn.credentials
import json


def get_results_from_API(string):
    r = requests.get("https://openapi.naver.com/v1/search/book.json",
                     headers=bfn.credentials.api,
                     params={
                         "query": string,
                         "start": 1,
                         "display": 100,
                     })
    y = json.loads(r.text)
    items = y["items"]
    for i in items:
        i["isbn"] = i["isbn"].split()[-1]
    return items