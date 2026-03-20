from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from cron.schedules import schedule_map
from controllers.utils import Utils

utils = Utils()
pp = utils.pretty_print
throw = utils.throw

class CeleryConfig:
    def __init__(self):
        self.app_name = 'multitenancy'
        self.settings_module = 'multitenancy.settings'
        self.schedule_map = schedule_map

    def configure(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', self.settings_module)
        app = Celery(self.app_name)
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.conf.broker_connection_retry_on_startup = True
        app.autodiscover_tasks()
        app.conf.beat_schedule = {**self.schedule_map}
        return app
celery_config = CeleryConfig()
app = celery_config.configure()