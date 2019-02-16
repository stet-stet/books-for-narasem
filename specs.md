# tools I will use

* **language: python 3.6**
* this API(https://developers.naver.com/docs/search/book/)
* Django-REST framework (+PostgreSQL)
* python-requests
* an AWS server.

# models 

## Books

* the books listed here
     * show up on the API described here(https://developers.naver.com/docs/search/book/)
     * are **sold** at Kyobobooks( www.kyobobook.co.kr ),
     * are about **statistics** (with a few exceptions),
     * but are **not** owned by Narasem Library(721 Eonju-ro, Gangnam-Gu, Seoul, South Korea)
* database fields
     * **ISBN**
     * Book title
     * Author
     * Publisher
     * Year published
     * price(at Kyobo bookstores)
     * the keyword used to search this book.
* the whole list will be returned in **.csv** as well as .json
     * this is because the list must be copied into Microsoft Excel.
* **Requirement: deletion of entries associated with certain keywords.**

## FailedBooks

* the books listed here
    * show up on the aforementioned API
    * but fail to satisfy one or more criteria.
* database fields
    * **ISBN**
    * Book title
    * the criterion it failed to meet
* the model will provide access to
    * the original titles of the books(.json and .csv)
    * list of entries not sold at Kyobo(.json and .csv)
    * list of entries sold at Kyobo but in the library(.json and .csv)
    

# Mechanism

1. User provides a keyword to the server by accessing finished API.
2. The back-end(?) searches the NAVER BOOKS API using the keyword.
    * It gathers the results into a single python set A.
3. Receive the full list of FailedBooks and Books, A -= FailedBooks, A -= Books.
4. For each item, check Kyobo to see if item is sold.
    * We use http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=**(ISBN HERE)**&orderClick=LAG&Kc=
    * If it's not being sold, put it in FailedBooks(crit="Kyobo")
    * If it is, gather data as appropriate, then take a quick look at Narasem Lib.(Use http://lib1.kostat.go.kr/)
        * If the book's there, put it in FailedBooks(crit="Narasem")
        * If it's not, then put it in Books(with appropriate data)
5. User may retrieve needed data which may include:
    * the whole list of Books, .csv
    * the whole list of unsold-at-Kyobo Books , .csv
6. User may choose to delete/wipe
    * the whole list of FailedBooks
    * Some Books found by a certain keyword.
7. Remember, **the user does not have access to anything except Chrome and Excel.**


# comments
The library doesn't provide ISBN data. Unbelievable.
This complicates things a lot. 

# deadline
2019.2.18(Mon)

# policy

I will turn this repo private as I commit the bit containing Naver API Client ID/Secret.
I will some reusable components in a separate repo.
