from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re
import urllib.parse
import pandas as pd


def request_soup(link):
    #downloads webpage data 
    req = Request(link)
    html_page = urlopen(req)
    #loads it in a BeautifulSoup object
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

all_songs = pd.DataFrame(columns=['Song_title','Song_interpret','City_name'])
city_names = [["Köln","Colonia", "Kölle", "Domstadt"], ["Bonn"]]

#"Stadt am Rhing", "Stadt met K"
for city_name in city_names:
    print(city_name)
    for name in city_name:
        print(name)
        link = f"https://musikguru.de/search/?q={urllib.parse.quote(name)}&t=songs"
        pages_total = request_soup(link).find("div", {"id": "PaginationInfo"}).get_text().split(" ")[-1]
        song_titles = []
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
                        #check that songtext name or lyrics contain the city name, if this is the case append songtext name and interpret to list
                        link = f"https://musikguru.de/{songtext_link}"
                        #get song_title and remove all unneccessary words from title
                        song_title = request_soup(link).find("div", {"id": "LyricsTitle"}).get_text().replace("Songtext", "").replace("Übersetzung", "").replace("Lyrics","")
                        song_interpret = request_soup(link).find("div", {"id": "LyricsArtistTitle"}).get_text().replace("von", "")
                        song_text = request_soup(link).find("div", {"id": "Lyrics"}).get_text()
                        if name in song_title or name in song_text:
                            all_songs = all_songs.append({"Song_title": song_title, "Song_interpret": song_interpret,"City_name": city_name[0]},ignore_index=True)


print(all_songs)


###Next steps:
### check for duplicate entries in dataframe
### make visualizations (histogramm)
### use songtexts from another website !