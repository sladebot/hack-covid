import feedparser
from app.sentiment_analyser import SentimentAnalyser

DEFAULT_FEEDS = ["http://rss.cnn.com/rss/cnn_topstories.rss",
                 "http://www.yahoo.com/news/rss/world",
                 "http://feeds.bbci.co.uk/news/world/rss.xml",
                 "http://feeds.reuters.com/Reuters/domesticNews"]

class RssConsumer:
    __feeds = DEFAULT_FEEDS
    __feeds_analyser = SentimentAnalyser()

    def __init__(self, feeds=None):
        if feeds is None:
            feeds = DEFAULT_FEEDS
            self.__feeds = feeds

    def __parse(self, feed_url):
        d = feedparser.parse(feed_url)
        articles = []
        for entry in d.entries:
            article = {
                'title': entry.get("title", ""),
                'description': entry.get("description", ""),
                'link': entry.get("link", ""),
                'pubData': entry.get("pubData", "")
            }
            articles.append(article)
    
        return articles

    def get_feeds(self):
        collector = []
        for feed in self.__feeds:
            __parsed_feed = self.__parse(feed)
            collector.append(__parsed_feed)
        return collector

