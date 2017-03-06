import psycopg2
from lxml import html, etree
import requests
import extractors
import time
import random


class crawl_item:
    def __init__(self, db_entry):
        self.id = db_entry[0]
        self.link = db_entry[1]
        self.id_feed = db_entry[2]


def run_crawl():
    with open('constring.txt') as f:
        connstring = f.readline()
    connpg = psycopg2.connect(connstring)
    cursorpg = connpg.cursor()

    #Retrieve selection of uncrawled entries uncrawled entries
    cursorpg.execute("""SELECT id, link, id_feed FROM entry WHERE entry.accessed = FALSE AND id_feed IN (3, 4, 7, 9, 13, 14, 15, 16, 17, 18, 79, 97, 98, 99, 100, 104, 105, 106, 111) ORDER BY DATE DESC LIMIT 50""")
    db_entries = cursorpg.fetchall()
    crawl_items = []

    for db_entry in db_entries:
        crawl_items.append(crawl_item(db_entry))

    random.shuffle(crawl_items)

    for item in crawl_items:
        crawl_text = extractors.dparser(item.link, item.id_feed) #might be none
        if crawl_text:
            cursorpg.execute("""UPDATE entry SET accessed = TRUE, scrape = %s, scrape_success = TRUE WHERE id = %s;""", (crawl_text, item.id))
        else:
            cursorpg.execute("""UPDATE entry SET accessed = TRUE, scrape_success = FALSE WHERE id = %s;""", (item.id,))
        print(item.link)
        print(crawl_text)
        time.sleep(2)
    
    connpg.commit()
    connpg.close()

def main():
    while True:
        run_crawl()
        time.sleep(15)

if __name__ == '__main__':
    main()