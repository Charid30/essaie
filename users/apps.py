from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    #5S5IKB6Bjl@example.com
    def ready(self):
        import users.signals
