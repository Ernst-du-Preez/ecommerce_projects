from django.apps import AppConfig

class EcommerceConfig(AppConfig):
    name = "ecommerce"

    def ready(self):
        # import signals so they are registered
        import ecommerce.signals  # noqa
