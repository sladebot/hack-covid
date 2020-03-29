from feedgen.feed import FeedGenerator

class RssGenerator:
    @staticmethod
    def generate(articles):
        fg = FeedGenerator()

        fg.title("Demo")
        fg.description("Demo")
        fg.language("en")
        fg.link(href='https://awesome.com')
        for a in articles:
            fe = fg.add_entry()
            fe.title(a["title"])
            fe.description(a["description"])

        return fg.rss_str()
