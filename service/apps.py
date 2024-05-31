from time import sleep

from django.apps import AppConfig


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'

    # def ready(self):
    #     from service.services import run_apscheduler
    #     sleep(2)
    #     run_apscheduler()
