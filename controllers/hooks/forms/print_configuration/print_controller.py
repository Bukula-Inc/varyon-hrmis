from controllers.utils import Utils

utils = Utils ()

def on_print_config_save(dbms, object):
    object.body.name = object.body.app_model