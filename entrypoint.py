"""Script to scrape the data and place it to database"""
import subprocess
import sys
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from news.scraping.sites.rss import GoogleRss


MONGO_CLIENT = 'mongodb://localhost:27017/'
NEWS_DB_NAME = 'news-db'
COLLECTION_NAME = 'google-rss'
DEFAULT_DUMP_FILE = 'news.csv'

def get_documents(feed):
    """Transform newsfeed to list of documents to paste

    Params
    ------
    feed
        scrapable news source
    """

    news = feed.scrape()
    return [onenew.document() for onenew in news]

def load_documents(collection, news):
    """Save news to mongo db collection

    Params
    ------
    collection
        mongo db collection
    news
        list of news documents to save
    """

    try:
        collection.insert_many(news, ordered=False)
    except BulkWriteError:
        pass

def start_mongo():
    """Starts mongo db"""

    try:
        subprocess.run(['mongod'], check=True)
    except subprocess.CalledProcessError:
        print('Failed, but most likely mongo is already started')

def dump_csv():
    """Dumps mongo collection to csv"""

    csv_file = input(f'Which file? ({DEFAULT_DUMP_FILE})\n') \
            or DEFAULT_DUMP_FILE

    cmd = [
        'mongoexport',
        f'--collection={COLLECTION_NAME}',
        f'--db={NEWS_DB_NAME}',
        f'--out={csv_file}',
        f'--uri={MONGO_CLIENT}',
        '--type=csv',
        '--fields=pubtime,title,link,description,body'
    ]

    subprocess.run(cmd, check=True)

def ask(collection, feed):
    """User interface

    Params
    ------
    collection
        mongo db collection
    feed
        scrapable news source
    """

    question = 'What do you want?\n' \
               '[0] - run mongo\n' \
               '[1] - scrape site\n' \
               '[2] - dump data\n' \
               '[q] - exit\n'

    answer = input(question)
    if answer == '0':
        start_mongo()
    elif answer == '1':
        news = get_documents(feed)
        load_documents(collection, news)
    elif answer == '2':
        dump_csv()
    elif answer == 'q':
        sys.exit()


if __name__ == "__main__":
    client = MongoClient(MONGO_CLIENT)
    newsdb = client[NEWS_DB_NAME]
    googlecoll = newsdb[COLLECTION_NAME]
    newsfeed = GoogleRss()

    while True:
        ask(googlecoll, newsfeed)
