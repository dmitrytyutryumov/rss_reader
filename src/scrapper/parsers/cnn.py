from src.scrapper.parsers.base import RSSParser


class CnnParser(RSSParser):
    source = "http://rss.cnn.com/rss/edition.rss"
