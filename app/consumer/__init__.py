import feedparser

class RssConsumer:
    __feeds = ["http://rss.cnn.com/rss/cnn_topstories.rss"]

    def __init__(self, feeds=None):
        if feeds is None:
            feeds = ["http://rss.cnn.com/rss/cnn_topstories.rss"]
        self.__feeds = feeds

    def __parse(self, feed_url):
        d = feedparser.parse(feed_url)
        articles = []

        for entry in d.entries:
            article = {
                'title': entry['title'],
                'description': entry['description'],
                'link': entry['link'],
            }
            articles.append(article)
        return articles

    def get_feeds(self):
        collector = []
        for feed in self.__feeds:
            __parsed_feed = self.__parse(feed)
            collector.append(__parsed_feed)
        return collector
