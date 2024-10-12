# -*- coding: utf-8 -*-
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seeds initial data for the application."

    def __init__(self):
        self.user_class = get_user_model()

        super().__init__()

    def handle(self, *args, **options):
        self.all_apps_make_migration()
        self.migrate()

    def all_apps_make_migration(self):
        for app in apps.get_app_configs():
            call_command("makemigrations", app.label)
            self.stdout.write("Created {} migration.".format(app.label))

    def migrate(self):
        call_command("migrate")
