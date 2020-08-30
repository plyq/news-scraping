"""Library of rss sites"""
from datetime import datetime
from lxml import etree, html
from news.scraping.site import ScrapingSite
from news.news import News


class GoogleRss(ScrapingSite):
    """Google RSS site"""

    URL = 'https://news.google.com/rss'
    ENCODING = 'UTF-8'
    DATEFMT = '%a, %d %b %Y %H:%M:%S GMT'
    TAGMAP = {
        'title': 'title',
        'description': 'description',
        'pubdate': 'pubDate',
        'link': 'link'
    }

    def __init__(self):

        super().__init__(self.URL)

    def scrape(self):
        """Get RSS parsed google feed

        Returns
        -------
        list
            of parsed News
        """

        root = etree.fromstring(str(self).encode(self.ENCODING))
        items = root.xpath('//item')
        news = []

        for item in items:
            data = self._news_item_scrape(item)
            news.append(News(**data))

        return news

    def _news_item_scrape(self, item):
        """Parse one news item

        Params
        ------
        item
            xml node

        Return
        ------
        dict
            with parsed data
        """

        data = {}

        for prop, tag in self.TAGMAP.items():
            value = item.find(tag)

            if value is None:
                continue

            value = value.text

            if tag == 'pubDate':
                value = self._strptime(value)

            elif tag == 'description':
                value = self._remove_html_markdown(value)

            data[prop] = value

        return data

    def _strptime(self, datestring):
        """Transfrom string to datetime object"""

        try:
            result = datetime.strptime(datestring, self.DATEFMT)
        except ValueError:
            result = datetime.now()

        return result

    @staticmethod
    def _remove_html_markdown(text):
        """Remove markdown from html text"""

        #TODO: not very accurate, need to improve
        htmlroot = html.fromstring(text)
        return htmlroot.text_content()
