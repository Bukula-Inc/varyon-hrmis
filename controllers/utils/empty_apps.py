from django.apps import apps
from django.core.management import call_command

# Get a list of all installed apps in your Django project
installed_apps = [app.name for app in apps.get_app_configs()]

# Iterate through each app and create empty migrations
for app_name in installed_apps:
    # Get the app's migrations module
    migrations_module = f'{app_name}.migrations'
    
    try:
        # Try to load the migrations module
        migrations = __import__(migrations_module, fromlist=['Migrations'])
    except ImportError:
        # If the app has no migrations module, move to the next app
        continue

    # Create an empty migration for the app
    call_command('makemigrations', app_name, empty=True)
