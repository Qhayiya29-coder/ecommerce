from django.apps import AppConfig


class CoreEcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_ecommerce'
    
    def ready(self):
        import core_ecommerce.signals  # noqa
