"""Module to represent News class"""


class News():
    """News class

    ...

    Properties
    ----------
    title : str
        news title
    description : str
        short news description
    pubdate : datetime
        datetime of news publication
    link : str
        link to full news page
    body:
        full news text
    """

    def __init__(
            self,
            **struct
    ):
        """
        Params
        ------
        **struct : dict
            full news content
        """

        self._info = struct

    @property
    def title(self):
        """Title"""
        return self._info.get('title', '')

    @property
    def description(self):
        """Short description"""
        return self._info.get('description', '')

    @property
    def pubdate(self):
        """Publication datetime"""
        return self._info.get('pubdate', None)

    @property
    def link(self):
        """Link to full news"""
        return self._info.get('link', '')

    @property
    def body(self):
        """Content of full news"""
        return self._info.get('body')

    @property
    def identity(self):
        """Key of uniqueness"""
        return {
            'title': self.title,
            'link' : self.link
        }

    def document(self):
        """Document to save to mongo db"""
        return {
            '_id': self.identity,
            'title': self.title,
            'link': self.link,
            'body': self.body,
            'pubdate': self.pubdate,
            'description': self.description
        }

    def __eq__(self, another):
        """Two news are equal if have the same id values"""
        return self.identity.values() == another.identity.values()

    def __str__(self):
        string = ''
        for prop, value in self._info.items():
            string += '{}:\n   {}\n'.format(prop, value)
        return string
