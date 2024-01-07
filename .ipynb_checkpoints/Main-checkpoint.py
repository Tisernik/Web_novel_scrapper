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



# Получаем html-текст страницы
r = requests.get(novel_link)
html_text = r.text
soup = BeautifulSoup(html_text,'html.parser')

# Вырезаем часть, в которой находятся ссылки на главы 
# при этом указаны ссылки не полностью, а только хвост, например "...href="/invincible-novel/chapter-1.html..."
a = soup.find_all("ul", class_="ul-list5")
soup2 = BeautifulSoup(str(a),'html.parser')

# Получение хвостов ссылок на главы книги
soup_links = soup2.find_all("a", class_="con")

# Проверка:
#soup_links[0].get('href')




# Собираем список с реальными ссылками на главы книги
i = 1
chapter_link = []
garbage = []
for chapter in soup_links:
    href_link_string = chapter.get('href')
    chapter_last_link = href_link_string[18:] # вырезаем из текста "/invincible-novel/chapter-3753.html" крайнее значение "hapter-3753.html"
    chapter_link.append(novel_link[:-5]+"/"+chapter_last_link)

    garbage.append(href_link_string)

# В общем случе раскоментить
# Вырзем первые 6 ссылок из-за указания последних загруженных глав
#chapter_link = chapter_link[6:]

# Выгрузить последние главы
chapter_link = chapter_link[-200:]



# Проходимся по главам и достаем оттуда текст

chapters = []
chapters_ = []

errors = []

k = 0
for iter_chapter in chapter_link:
    time.sleep(1)
    #print(iter_chapter)
    
    req_chapter_link = requests.get(iter_chapter)
    chapter_html_text = req_chapter_link.text
    chapter_soup = BeautifulSoup(chapter_html_text,'html.parser')    
    chapter_soup_text = str(chapter_html_text)
     
    # вырезаю split-ом из-за того, что при "find_all" существеная часть текста пропадает
    # Сразу чистим от </p>
    chapter_soup_text = chapter_soup_text.replace("</p>", "")
    
    chapter_soup_text = chapter_soup_text.replace("<strong><u>", "")
    chapter_soup_text = chapter_soup_text.replace("</u></strong> ", "")

    chapter_soup_text = chapter_soup_text.replace("<h4>", "")
    chapter_soup_text = chapter_soup_text.replace("</h4>", "")

    chapter_soup_text = chapter_soup_text.replace("<b></b> ", "")

    chapter_soup_text = chapter_soup_text.replace("</div>", "")
    
    chapter_soup_text2 = chapter_soup_text.split("<div id=\"article\">")
    
    if len(chapter_soup_text2)>1:
        chapter_soup_text3 = chapter_soup_text2[1].split("<div class=\"notice-text\">")
        chapter_soup_text4 = chapter_soup_text3[0].split("<p>")
        ch_er = "Выполнение главы:" + iter_chapter
        errors.append(ch_er)
    else:
        print(iter_chapter)
        print(req_chapter_link)
        chapter_soup_text3 = ""
        chapter_soup_text4 = []
        ch_er = "!!! Проблемная глава:" + iter_chapter
        errors.append(ch_er)
    

    # вырезаем из строк типовое барахло "A day passed. <div style="margin-top: 0px; margin-botto%"
    new_txt = []
    for txt in chapter_soup_text4:
        txt_ = txt.split("<div style")

        # убираем пустые значения из списка абзацев в главе
        if txt_[0]!= "":
                 if txt != " ":
                     new_txt.append(txt_[0])
    
    chapters.append(new_txt)
    update_progress(k / len(chapter_link))
    print("Последняя глава:" + iter_chapter)
    k=k+1



book = FictionBook2()

title = 'INVINCIBLE'
book.titleInfo.title = title
book.documentInfo.version = "1.1"

book.chapters = []

for i in chapters:
    book.chapters.append((i[0], i[1:]))

book.write(title + ".fb2")