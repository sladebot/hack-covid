import os

from app import init_app
from flask_script import Manager, Server

app = init_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
manager.add_command("runserver", Server(host=app.config.get('HOST'), port=app.config.get('PORT')))

if __name__ == "__main__":
    manager.run()

