import requests
from bs4 import BeautifulSoup
from time import sleep

def bookinfo_from_kyobo(isbn):
    r = requests.get("http://www.kyobobook.co.kr/product/detailViewKor.laf",
                     params={
                         "ejkGb": "KOR",
                         "mallGb": "KOR",
                         "barcode": str(isbn),
                         "orderClick": "LET",
                         "Kc": "",
                     },
                     headers={
                         'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'en-US,en;q=0.5',
                         'Accept': "*/*",
                         'Connection': 'keep-alive',
                     })
    # print(isbn)
    # print("------------")
    # print(r.text.length)
    # print("------------")
    # print(r.request.headers)
    # print("------------")
    # print(r.headers)
    # print("------------")
    # a = input()
    # sleep(5)
    if r.text.find(u'요청하신 페이지를') > 0:
        print("Not found.")
        return None
    else:
        ret = {}
        try:
            bsObj = BeautifulSoup(r.text, 'html.parser')
            print(len(bsObj.get_text()))
            # isbn
            ret['isbn'] = isbn
            ret['price'] = bsObj.find_all("span", class_="org_price")[0].get_text().strip().strip('원')
            # title
            ret['title'] = bsObj.find_all("meta", property="og:title")[0]["content"]
            data_bundle = bsObj.find_all("div", class_="author")[0]
            ret['publisher']=data_bundle.find("span", class_="name", title="출판사").get_text().strip()
            authorTemp = bsObj.find("div", class_="title_detail_author").h3.get_text().strip()
            ret['author'] = authorTemp[authorTemp.find(':')+1:].strip()
            ret['year'] = data_bundle.find("span", class_="date", title="출간일").get_text().strip().split(' ')[0]
            print(repr(ret)+"hell.")
        except IndexError:
            print("wrong index!")
        finally:
            return ret




        # data: isbn, book title, author, publisher, year, price, (keyword)
        # the 갯수?

"""
from bfn.scraputil.Kyobo import bookinfo_from_kyobo
bookinfo_from_kyobo(9788968484698)
"""