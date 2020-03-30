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
            if(a['Giphy']):
                description = a["description"] + "<img src=\"{}\" border=\"0\"></img>".format(a['Giphy'])
            else:
                description = a["description"]
            fe = fg.add_entry()
            fe.title(a["title"])
            fe.description(description)
            if 'image' in a:
                fe.enclosure(url=a['image'], type=a['mime_type'])
            fe.link(href=a['link'])

        return fg.rss_str()
