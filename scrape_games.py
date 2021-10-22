import requests
from bs4 import BeautifulSoup

url = "https://old.chesstempo.com/game-database.html"
endpoint = "https://old.chesstempo.com/requests/gameslist.php?"

#startIndex=0&results=50&currentFen=rnbqkbnr%2Fpppppppp%2F8%2F8%2F8%2F8%2FPPPPPPPP%2FRNBQKBNR%20w%20KQkq%20-%200%201&sort=avgelo&dir=desc&pieceColour=either&gameResult=any&subsetMinRating=2200&gamesForPos=1

data = {
    'startIndex' : 0,
    'results' : 500,
    'sort' : 'avgelo',
    'dir' : 'desc',
    'pieceColour' : 'either',
    'gameResult' : 'any',
    'subsetMinRating' : 2200,
    'gameForPos' : 1,
}

response = requests.post(url=endpoint, data=data)
soup = BeautifulSoup(response.text, "lxml")

tables = soup.find_all("tbody", {"class":"yui-dt-data"})
print(tables)

print(soup.prettify())
