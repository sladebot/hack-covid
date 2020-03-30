from flask import Flask
from flask import make_response, jsonify
from app.config.config import config
from app.sentiment_analyser import SentimentAnalyser
from app.consumer import RssConsumer
from app.generator import RssGenerator
from app.giphy import GiphyAPI

def init_app(config_name):
    app = Flask(__name__)
    rss_consumer = RssConsumer()
    app.config.from_object(config[config_name])


    @app.route('/')
    def home_page():
        res = {
            'success': True
        }
        return jsonify(res)

    @app.route('/rss')
    def rss():
        articles_from_feeds_from_sources = rss_consumer.get_feeds()
        feeds_from_analyser = []
        for articles in articles_from_feeds_from_sources:
            feeds_from_analyser.append(feeds_analyser.get_sentiment_scores(articles))
        ## Call analysis here and filter and only pass filtered articles. For now, add everything
        filtered_articles = []
        for feed_articles in feeds_from_analyser:
            filtered_articles += feed_articles

        rss_str = RssGenerator.generate(filtered_articles)
        res = make_response(rss_str)
        res.headers.set('Content-Type', 'application/rss+xml')

        return res

    return app
