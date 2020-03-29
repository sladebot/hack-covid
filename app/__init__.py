from flask import Flask
from flask import make_response, render_template, jsonify, url_for
from app.config.config import config
from app.consumer import RssConsumer
from app.generator import RssGenerator


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
        articles_from_feeds = rss_consumer.get_feeds()
        ## Call analysis here and filter and only pass filtered articles 
        rss_str = RssGenerator.generate(articles_from_feeds[0])
        res = make_response(rss_str)
        res.headers.set('Content-Type', 'application/rss+xml')
        return res

    @app.errorhandler(500)
    def server_error(error=None):
        return render_template('500.html')

    @app.errorhandler(404)
    def not_found(error=None):
        return render_template('404.html')

    return app
