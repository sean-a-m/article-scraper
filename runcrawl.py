import time
import scraper

def main():
    article_scraper = scraper()
    while True:
        pending_entries = article_scraper.get_pending()
        if pending_entries.size:
            print("Reading " + str(len(pending_entries)) + "pending entries")
            for entry in pending_entries:
                scraper.scrape_entry(entry)
                time.sleep(2)
        else:
            print("No new pending entries")
            time.sleep(60)

if __name__ == '__main__':
    main()
