#!./.venv/bin/ python
import os, sys
from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
# from celery import Celery, platforms, Task
# from celery.bin.worker import main as worker_main


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


# class BoundTask(Task):
#     abstract = True
#
#     def __call__(self, *args, **kwargs):
#         if app.config.get('CELERY_ALWAYS_EAGER'):
#             return super(BoundTask, self).__call__(*args, **kwargs)
#         else:
#             with app.app_context():
#                 print('***** flask app context injected *****')
#                 db.session.flush()
#                 return super(BoundTask, self).__call__(*args, **kwargs)
#
# celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
#                 broker=app.config['CELERY_BROKER_URL'],
#                 set_as_current=True, task_cls=BoundTask)
# celery.conf.update(app.config)


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(port=8088))


# @manager.command
# def worker(loglevel='info'):
#     """Run celery worker."""
#
#     # platforms.C_FORCE_ROOT = True  # need root to run celery, change it
#
#     sys.argv = [sys.argv[0], '-l', loglevel, '-E']
#     worker_main(celery)


if __name__ == '__main__':
    manager.run()