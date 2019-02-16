import requests
from bs4 import BeautifulSoup
from time import sleep

def search_narasem(title,author,year):
    headers={
        "Accept": "text/html",
        "Accept-encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "lib1.kostat.go.kr",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv=65.0;) Gecko/20100101 Firefox/65.0"
    }
    s = requests.Session()
    s.get("http://lib1.kostat.go.kr/")
    s.headers = headers
    s.params = {"st":"KWRD", "si":"TOTAL", "q":' '.join([title,author])}
    r = s.get("http://lib1.kostat.go.kr/search/tot/result", timeout=20)
    sleep(3)
    return r.text.find("divNoResult") == -1

