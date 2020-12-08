from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
"""
manage.py -  migrates the Flask SQLAlchemy db to the production db when called.
"""
migrate = Migrate(app, db)
db.init_app(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()