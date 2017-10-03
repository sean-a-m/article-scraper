import psycopg2
import configparser
import random
import sys
import extractors

class scraper:

    class scrape_item:
        def __init__(self, db_entry):
            self.id = db_entry[0]
            self.link = db_entry[1]
            self.id_feed = db_entry[2]

    def get_pending(self):
        """Retrieve a list of the most recent entries that haven't been scraped yet"""
        pending_entries = []
        try:
            self.cursor.execute("""SELECT id, link, id_feed FROM entry WHERE entry.accessed = FALSE AND id_feed IN (SELECT id FROM selectedfeeds) ORDER BY DATE DESC LIMIT 50;""")
            db_entries = self.cursor.fetchall()
            for db_entry in db_entries:
                pending_entries.append(self.scrape_item(db_entry))
            #quick fix to sometimes avoid hitting same site repeatedly, maybe
            random.shuffle(pending_entries)
        except:
            #TODO: log this somewhere
            print("Unexpected exception (Fix Me!):", sys.exc_info()[0])
        finally:
            return pending_entries

    def scrape_entry(self, entry):
        crawl_text = extractors.dparser(entry.link, entry.id_feed)  # might be none
        if crawl_text:
            try:
                self.cursor.execute("""UPDATE entry SET accessed = TRUE, scrape = %s, scrape_success = TRUE WHERE id = %s;""", (crawl_text, entry.id))
            except:
                # TODO: log this somewhere
                print("Unexpected exception (Fix Me!):", sys.exc_info()[0])
        else:
            try:
                self.cursor.execute("""UPDATE entry SET accessed = TRUE, scrape_success = FALSE WHERE id = %s;""",(entry.id,))
            except:
                # TODO: log this somewhere
                print("Unexpected exception (Fix Me!):", sys.exc_info()[0])

        self.connection.commit()

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf')
        db_config = config['database']
        connection_string = "host={0} dbname={1} user={2} password={3} port={4}".format(db_config['host'], db_config['dbname'], db_config['user'], db_config['password'], db_config['port'])
        self.connection = psycopg2.connect(connection_string)
        self.cursor = self.connection.cursor()
