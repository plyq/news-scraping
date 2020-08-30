"""Script to scrape the data and place it to database"""
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from news.scraping.sites.rss import GoogleRss


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

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    newsdb = client['news-db']
    googlecoll = newsdb['google-rss']

    newsfeed = GoogleRss()

    docs = get_documents(newsfeed)
    load_documents(googlecoll, docs)
