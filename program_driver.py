import requests

def drive():
    words=["통계","수학","베이지언","유의성","SPSS","전후비교","표본","tukey","군집","동질성"]
    for i in words:
        r = requests.get("http://127.0.0.1:8000/search/"+str(i)+"/")
        print(r.content)


if __name__=="__main__":
    drive()