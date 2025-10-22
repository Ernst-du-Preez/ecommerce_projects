# ecommerce/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Store, Product
from .twitter_client import post_tweet

@receiver(post_save, sender=Store)
def tweet_on_new_store(sender, instance, created, **kwargs):
    if not created:
        return
    name = instance.name
    desc = (instance.description or "").strip()
    message = f"🛍️ New Store: {name}\n{desc}" if desc else f"🛍️ New Store: {name}"
    image = instance.logo if getattr(instance, 'logo', None) else None
    post_tweet(message, image_field=image)

@receiver(post_save, sender=Product)
def tweet_on_new_product(sender, instance, created, **kwargs):
    if not created:
        return
    store_name = instance.store.name
    message = f"🆕 New Product from {store_name}\n{instance.name}\n{(instance.description or '')}"
    image = instance.image if getattr(instance, 'image', None) else None
    post_tweet(message, image_field=image)
