# create a book title 'only-i-am-a-necromancer' and download all chapters

import os
from gtts import gTTS
import requests
from bs4 import BeautifulSoup

# raise exception if status_code is not 200
base_URL: str = 'https://lightnovelreader.me/only-i-am-a-necromancer/chapter-'
book_title: str = 'only-i-a-necromancer-html'


def downloadChapter(url: str, chapter: int) -> str:

    r = requests.get(url+str(chapter))
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', id='chapterText')
    return div


def textChapter(div) -> str:

    text = div.get_text()
    # delete all occurences of 'SPONSORED CONTENT' in the text and ignore case
    text = text.lower().replace('sponsored content', '')
    text = text.replace(".", ".\n")
    return text


def cleanChapter(div):

    extraContents = div.findAll('p')
    extraContents += div.findAll('center')
    extraContents += div.findAll('div', class_='hidden')
    for content in extraContents:
        content.extract()

    # add header 2  to the beginging  of div
    return div


def writeChapter(book_title: str, text: str, chapter: int):
    with open(f"{book_title}/chapter_{chapter}.tex", 'w', encoding="utf-8") as f:
        f.write('\section{chapter '+str(chapter)+'}\n')
        f.write(text)


HTML_DOC = """
              <html>
               <head>
                   <title> Add new Tag </title>
               </head>
               <body>
                       <div id='chapters'> This is a paragraph. </div>
               </body>
             </html>
            """


def downloadBook(base_URL: str, book_title: str):
    """ The code above does the following, explained in English:
1. Create a new directory with the name of the book
2. Download the first chapter of the book
3. Save the first chapter of the book
4. Download the second chapter of the book
5. Save the second chapter of the book
6. Repeat steps 4-5 until there are no more chapters """
    # os.mkdir(book_title)

    chapter: int = 332
    soup = BeautifulSoup(HTML_DOC, "html.parser")
    body = soup.find('div', id='chapters')
    while chapter < 512:
        content = downloadChapter(base_URL, chapter)
        content = cleanChapter(content)
        h2 = soup.new_tag("h2", id="chapter"+str(chapter))
        h2.string = "Chapter " + str(chapter)
        body.append(h2)
        body.append(content)
        chapter += 1

    # with open(f"only-i-a-necromancer-html/{book_title}.html", 'w', encoding="utf-8") as f:
    #     f.write(str(soup))


downloadBook(base_URL, book_title)
