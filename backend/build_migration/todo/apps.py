from django.apps import AppConfig


class TodoConfig(AppConfig):
    name = "build_migration.todo"
    verbose_name = "Todo"

    def ready(self):
        """
        Override this to put in:
        - Users system checks
        - Users signal registration
        """
