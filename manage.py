import os
#from app import create_app, db
from app import create_app, mongo
from app.models import *
from flask_script import Manager, Shell
#from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
#migrate = Migrate(app, db)


def make_shell_context():
    #return dict(app=app, mongo=mongo, User=User, Role=Role, Permission=Permission, Post=Post, Comment=Comment)
    return dict(app=app, mongo=mongo, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
#manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()