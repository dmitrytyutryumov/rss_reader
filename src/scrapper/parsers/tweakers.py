from src.scrapper.parsers.base import RSSParser


class TweakersParser(RSSParser):
    source = "https://feeds.feedburner.com/tweakers/mixed"
