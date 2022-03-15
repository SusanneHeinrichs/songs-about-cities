from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re
import urllib.parse


def request_soup(link):
    #downloads webpage data 
    req = Request(link)
    html_page = urlopen(req)
    #loads it in a BeautifulSoup object
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

names_köln = ["Köln"]
for name in names_köln:
    link = f"https://musikguru.de/search/?q={urllib.parse.quote(name)}&t=songs"
    pages_total = request_soup(link).find("div", {"id": "PaginationInfo"}).get_text().split(" ")[-1]
    links = []
    page = 1
    
    while page != int(pages_total) + 1:
        if page == 1:
            pass
        else:
            link = f"https://musikguru.de/search/?q={urllib.parse.quote(name)}&t=songs&p={page}"
        soup = request_soup(link)
        page += 1
        #gets all links and appends them to a list ('a' is indicator for links in html)
        for link in soup.findAll('a'):
            songtext_link = link.get('href')
            #append only links that are directing to a songtext
            if "html" in songtext_link:
                if songtext_link.split("/")[2].split("-")[0] == "songtext":
                    links.append(songtext_link)
        print(links)

    """
    # amount of list item childs inside the pagination list that we dont care about
    paginationListBullshitListElementsOffset = 2

    currentPage = 1

    paginationList = soup.find('.listPagingNavigator')
    nextPageItem = paginationList.select_one(":nth-child(" + str(paginationListBullshitListElementsOffset + currentPage + 1) + ")")
    currentPage = currentPage + 1
    nextPageLink = nextPageItem.select_one('a')
    """

    """
    page = requests.get(f"https://www.songtexte.com/search?q={name}&c=songs")
    soup = BeautifulSoup(page.content, 'html.parser')
    all_songs = soup.find_all('span', class_='song')
    for song in all_songs:
        print(song.get_text())
        ###go to songtext and verify that the city name is part of the title/songtext if not do not add songtext name to dataframe
    """

###Next steps

### Go through all pages of the query result 
### 