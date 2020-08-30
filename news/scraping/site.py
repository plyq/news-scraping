"""Describes abstract class ScrapingSite"""
from abc import ABCMeta, abstractmethod
import requests

class ScrapingSite(metaclass=ABCMeta):
    """Abstract class for all sites to scrape

    ...

    Attributes
    ----------
    url : str
        link to the site content
    encoding : str
        site encoding

    Methods
    -------
    scrape
        abstact method to convert site content to interested dictionary

    __str__
        shows content of the site as string
    """

    def __init__(self, url):
        """
        Params
        ------
        url : str
            site url
        encoding : str
            site encoding
        """

        self._url = url

    @property
    def url(self):
        """Site url"""

        return self._url

    def response(self):
        """GET response from site"""

        response = requests.get(self.url)
        return response

    def __str__(self):
        """str(ScrapingSite) returns content of this site"""

        content = self.response().text
        return content

    @abstractmethod
    def scrape(self):
        """Method to get interested site content

        Raises
        ------
        NotImplementedError
            If method is not implemented in subclass
        """

        raise NotImplementedError('"scrape" method was not found')
