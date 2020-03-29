from flask import Flask
from flask import render_template, redirect, jsonify, url_for
from app.config.config import config


def init_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.route('/')
    def home_page():
        res = {
            'success': True
        }
        return jsonify(res)



    @app.errorhandler(500)
    def server_error(error=None):
        return render_template('500.html')

    @app.errorhandler(404)
    def not_found(error=None):
        return render_template('404.html')

    return app
