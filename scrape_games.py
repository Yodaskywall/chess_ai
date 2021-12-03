import requests
from bs4 import BeautifulSoup

url = "https://old.chesstempo.com/game-database.html"
endpoint = "https://old.chesstempo.com/requests/gameslist.php"

#startIndex=0&results=50&currentFen=rnbqkbnr%2Fpppppppp%2F8%2F8%2F8%2F8%2FPPPPPPPP%2FRNBQKBNR%20w%20KQkq%20-%200%201&sort=avgelo&dir=desc&pieceColour=either&gameResult=any&subsetMinRating=2200&gamesForPos=1

data = {
    'startIndex' : 0,
    'results' : 500,
    'sort' : 'avgelo',
    'dir' : 'desc',
    'pieceColour' : 'either',
    'gameResult' : 'any',
    'subsetMinRating' : 2200,
}


cookies = { 'PHPSESSID' : 'l79u5esvijeamojntg3mcffsvv'}

headers = {
    "cookie" : "PHPSESSID=l79u5esvijeamojntg3mcffsvv",
    "user-agent" : "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "accept" : "*/*",
}

response = requests.post(url=endpoint, params=data, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, "lxml")

tables = soup.find_all("tbody", {"class":"yui-dt-data"})
print(tables)

print(soup.prettify())
with open("pito.html", "w") as file:
    text = soup.text.split("\n")
    for line in text:
        try:
            file.write(line)
        except:
            print(line)
            print("xd")

