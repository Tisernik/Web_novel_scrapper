import requests 
import numpy as np
import io
import os
from bs4 import BeautifulSoup
from FB2 import FictionBook2, Author
from urllib import request
import time, sys
from IPython.display import clear_output


novel_link = 'https://freewebnovel.com/invincible-novel.html'

# нужно поделить ссылку на составные части, чтобы вырезать 

r = requests.get(novel_link)
html_text = r.text
soup = BeautifulSoup(html_text,'html.parser')

# Получение ссылок на главы книги
soup_links = soup.find_all("a", class_="con")

print(soup_links[1])

soup_links[1].get('href')

soup_chapter_titles = soup.find_all("li", title)

def update_progress(progress):
    bar_length = 20
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))

    clear_output(wait = True)
    text = "Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
    print(text)




book = FictionBook2()

# Получение названия книги
title = soup.find("title")
title = str(title).replace("<title>Novel ", "")
title = title.replace(" - FastNovel</title>", "")
book.titleInfo.title = title

#book.titleInfo.annotation = "Small test book. Shows basics of FB2 library"
#book.titleInfo.authors = [Author(firstName="Alex", middleName="Unknown",nickname="Ae_Mc",emails=["ae_mc@mail.ru"],homePages=["ae-mc.ru"])]
#book.titleInfo.genres = ["sf", "sf_fantasy", "shortstory"]
#book.titleInfo.coverPageImages = [request.urlopen("https://picsum.photos/1080/1920").read()]
#book.titleInfo.sequences = [("Example books", 2)]
#book.documentInfo.authors = ["Ae Mc"]
book.documentInfo.version = "1.1"




link_list = []
titles_list = []

i = 1
for link in soup_links:
    link_text_1 = 'https://fastnovel.net/the-first-order3-3782'+link.get('href')
    link_titles = link.get('title')
    link_list.append([i, link_titles.replace("The First Order ", ""), link_text_1])
    i=i+1
    #if i == 3: break

chapter_entity=[]
chapters_ = []

book.chapters = []

k = 0
for link_i in link_list:
    req = requests.get(link_i[2])
    link_text = req.text
    link_soup = BeautifulSoup(link_text,'html.parser')
    chapter_text = link_soup.find_all("div", {"id": "chapter-body"})
    chapter_text = str(chapter_text)
    chapter_text = chapter_text.replace("</p><div", "</p> <div")
    chapter_text = chapter_text.replace("</div><p>", "</div> <p>")
    chapter_text = chapter_text.replace("\\", "")
    chapter_text = chapter_text.replace("Â\xa0 ", "")
    chapter_text = chapter_text.replace("â\xa0 ", "")
    chapter_text = chapter_text.replace("â\x80¦", "...")
    chapter_text = chapter_text.replace("â\x80\x94", "—")
    #chapter_text = chapter_text.replace("\\", "")
    #chapter_text = chapter_text.replace("\'s", " is")
    #chapter_text = chapter_text.replace("\'t", " not")
    #chapter_text = chapter_text.replace("\'re", " are")
    #chapter_text = chapter_text.replace("\'v", " have")
    #chapter_text = chapter_text.replace("\'m", "  am")
    #chapter_text = chapter_text.replace("\'ll", " will")
    chapter_text = chapter_text.replace("â\x80¦Â\xa0", "......")
    chapter_text_splitted = chapter_text.split("p>")
    

    l = ""
    chapter_text = list()
    for i in chapter_text_splitted:
        i = i.replace("</", "")
        i = i.replace("<", "")
        if i.find("div class") != -1:
            continue
        if i.find("[div id") != -1:
            continue
        if i == "div>]":
            continue
        if i == "":
            continue
        chapter_text.append(i)
    chapter_title = str(link_i[1])
    book.chapters.append((chapter_title, chapter_text))
    update_progress(k / len(link_list))
    k=k+1


update_progress(1)
book.write("TheFirsOrder.fb2")


