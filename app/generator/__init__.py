from feedgen.feed import FeedGenerator


class RssGenerator:

    @staticmethod
    def generate(articles):
        fg = FeedGenerator()

        fg.title("Sanity")
        fg.description("An emotionally balanced newsfeed")
        fg.language("en")
        fg.link(href='https://example.com', rel='alternate')
        for a in articles:
            fe = fg.add_entry()
            fe.title(a["title"])
            fe.description(a["description"])
            if 'image' in a:
                fe.enclosure(url=a['image'], type=a['mime_type'])
            # fe.enclosure(url="https://media.giphy.com/media/glvyCVWYJ21fq/giphy.gif", type="image/gif", length=11407941)
            fe.link(href=a['link'])

        return fg.rss_str()
