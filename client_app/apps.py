from django.apps import AppConfig
# from management import Defaults_Manager
from django.db.models.signals import post_migrate, pre_migrate
from django.dispatch import receiver
from controllers.utils import Utils
utils = Utils()

class ClientAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_app'

# # execute create defaults
# @receiver(post_migrate)
# def init_post_migration_action(sender, using="default", **kwargs):
#     Defaults_Manager.init_postmigration_actions(using, sender, **kwargs)