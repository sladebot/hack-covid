from feedgen.feed import FeedGenerator

class RssGenerator:
    @staticmethod
    def generate(articles):
        fg = FeedGenerator()

        fg.title("Sanity")
        fg.description("An emotionally balanced newsfeed")
        fg.language("en")
        fg.link(href='', rel='alternate')
        for a in articles:
            fe = fg.add_entry()
            fe.title(a["title"])
            fe.description(a["description"])


        return fg.rss_str()
