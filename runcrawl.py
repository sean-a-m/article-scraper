import psycopg2
from lxml import html, etree
import requests
import extractors
import time


class crawl_item:
    def __init__(self, db_entry):
        self.id = db_entry[0]
        self.link = db_entry[1]
        self.id_feed = db_entry[2]

def main():
    with open('constring.txt') as f:
        connstring = f.readline()
    connpg = psycopg2.connect(connstring)
    cursorpg = connpg.cursor()

    #Retrieve selection of uncrawled entries uncrawled entries
    cursorpg.execute("""SELECT id, link, id_feed FROM entry WHERE entry.accessed = FALSE AND id_feed IN (3, 4, 7, 9, 13, 14, 15, 16, 17, 18, 97, 98, 99, 100, 104, 105) ORDER BY DATE DESC LIMIT 10""")

    db_entries = cursorpg.fetchall()

    crawl_items = []

    for db_entry in db_entries:
        crawl_items.append(crawl_item(db_entry))

    for item in crawl_items[:50]:
        print(item.link)
        test_text = extractors.dparser(item.link, item.id_feed)
        print(test_text)
        time.sleep(2)

if __name__ == '__main__':
    main()