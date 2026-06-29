from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    
    def ready(self):
        # Import signals to ensure they are registered when app is ready.
        # Currently empty — will add signals later if needed.
        pass