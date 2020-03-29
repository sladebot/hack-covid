import os

from app import init_app

app = init_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == "__main__":
    app.run()
