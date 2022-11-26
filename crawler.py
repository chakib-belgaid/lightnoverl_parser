# create a book title 'only-i-am-a-necromancer' and download all chapters

import os
from gtts import gTTS
import requests
from bs4 import BeautifulSoup

# raise exception if status_code is not 200
base_URL: str = 'https://lightnovelreader.me/only-i-am-a-necromancer/chapter-'
book_title: str = 'only-i-a-necromancer'


def downloadChapter(url: str, chapter: int) -> str:
    """ The code above does the following:
1. It takes a URL and chapter number as input
2. It then downloads the HTML of the page
3. It then parses the HTML to get the text of the chapter
4. It then deletes all occurences of "sponsored content"
5. It then replaces all fullstops with a fullstop and a newline character
6. It returns the text of the chapter """
    r = requests.get(url+str(chapter))
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.find('div', id='chapterText').get_text()
    # delete all occurences of 'SPONSORED CONTENT' in the text and ignore case
    text = text.lower().replace('sponsored content', '')
    text = text.replace(".", ".\n")
    return text


def writeChapter(book_title: str, text: str, chapter: int):
    """ The code above does the following, explained in English:
1. Creates a file called 'chapter_1.tex' in the folder 'book_title'
2. Writes the text "\section{chapter 1}" to the file
3. Writes the text 'text' to the file """
    with open(f"{book_title}/chapter_{chapter}.tex", 'w', encoding="utf-8") as f:
        f.write('\section{chapter '+str(chapter)+'}\n')
        f.write(text)


def downloadBook(base_URL: str, book_title: str):
    """ The code above does the following, explained in English:
1. Create a new directory with the name of the book
2. Download the first chapter of the book
3. Save the first chapter of the book
4. Download the second chapter of the book
5. Save the second chapter of the book
6. Repeat steps 4-5 until there are no more chapters """
    os.mkdir(book_title)
    chapter: int = 1
    while True:
        text: str = downloadChapter(base_URL, chapter)
        writeChapter(book_title, text, chapter)
        chapter += 1


downloadBook(base_URL, book_title)
