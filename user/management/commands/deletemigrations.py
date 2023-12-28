# delete_all_migrations.py

import os
import shutil
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = "Deletes all migrations in the current Django project."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Deleting all migrations..."))

        # Assuming your Django project is in the same directory as this script
        project_path = os.getcwd()

        # Fetch all installed apps
        installed_apps = settings.INSTALLED_APPS

        for app in installed_apps:
            app_dir = app.split(".")[0]
            # Construct the migration directory path for each app
            migration_dir = os.path.join(project_path, app_dir, "migrations")
            self.stdout.write(
                self.style.HTTP_INFO(f"Migration Path Found: %s" % migration_dir)
            )

            # Check if the migrations directory exists
            if os.path.exists(migration_dir):
                self.stdout.write(
                    self.style.SUCCESS(f"Deleting migrations for app: {app}")
                )

                # Remove all files in the migrations directory
                for filename in os.listdir(migration_dir):
                    file_path = os.path.join(migration_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed to delete {file_path}. Reason: {e}"
                            )
                        )

                # Create an empty __init__.py file in the migrations directory
                init_file = os.path.join(migration_dir, "__init__.py")
                open(init_file, "w").close()

            else:
                self.stdout.write(
                    self.style.HTTP_INFO(f"No Migration Path Found: %s" % migration_dir)
                )

        # Run makemigrations to create new initial migrations
        # call_command("makemigrations")

        self.stdout.write(self.style.SUCCESS("All migrations deleted successfully."))
