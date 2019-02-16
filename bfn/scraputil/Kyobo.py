import requests
from bs4 import BeautifulSoup

def bookinfo_from_kyobo(isbn):
    isbn = 9788968484698
    r = requests.get("http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode="+repr(isbn)+"&orderClick=LET&Kc=")
    print(r.status_code)
    if r.text.find('class="title"') == -1:
        return None
    else:
        ret = {}
        try:
            bsObj = BeautifulSoup(r.text, 'html.parser')
            # isbn
            ret['isbn'] = isbn
            # title
            ret['title'] = bsObj.find_all("meta", property="og:title")[0]["content"]
            data_bundle = bsObj.find_all("div", class_="author")[0]
            ret['publisher']=data_bundle.find("span", class_="name", title="출판사").get_text().strip()
            authorTemp = bsObj.find("div", class_="title_detail_author").get_text().strip()
            ret['author'] = authorTemp[authorTemp.find(':')+1:].strip()
            ret['year'] = data_bundle.find("span", class_="date", title="출간일").get_text().strip().split(' ')[0]
            ret['price'] = bsObj.find_all("span", class_="org_price")[0].get_text().strip().strip('원')
            print(ret)
        finally:
            return ret




        # data: isbn, book title, author, publisher, year, price, (keyword)
        # the 갯수?

"""
from bfn.scraputil.Kyobo import bookinfo_from_kyobo
bookinfo_from_kyobo(9788968484698)
"""