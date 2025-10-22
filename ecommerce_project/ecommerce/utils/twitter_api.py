import tweepy
from django.conf import settings
import os

def get_twitter_client():
    """
    Creates and returns a Tweepy API client using credentials from settings.py
    """
    if not hasattr(settings, 'TWITTER_CONFIG'):
        return None
    config = settings.TWITTER_CONFIG
    auth = tweepy.OAuth1UserHandler(
        config["API_KEY"],
        config["API_SECRET"],
        config["ACCESS_TOKEN"],
        config["ACCESS_SECRET"]
    )
    return tweepy.API(auth)


def tweet_store(store):
    """
    Tweet when a new store is created.
    Includes store name, description, and logo (if available).
    """
    client = get_twitter_client()
    if not client:
        return  # Twitter not configured

    text = f"🛍 New Store Added!\n\nName: {store.name}\nDescription: {store.description}"

    try:
        media_ids = []
        if store.logo and os.path.isfile(store.logo.path):  # Check if logo exists
            media = client.media_upload(store.logo.path)
            media_ids.append(media.media_id)

        client.update_status(status=text, media_ids=media_ids if media_ids else None)
        print(f"Store tweet sent: {store.name}")
    except Exception as e:
        print(f"Error tweeting store: {e}")


def tweet_product(product):
    """
    Tweet when a new product is added.
    Includes store name, product name, description, and image (if available).
    """
    client = get_twitter_client()
    if not client:
        return  # Twitter not configured

    text = (
        f"🆕 New Product Added!\n\n"
        f"Store: {product.store.name}\n"
        f"Product: {product.name}\n"
        f"{product.description}"
    )

    try:
        media_ids = []
        if product.image and os.path.isfile(product.image.path):  # Check if image exists
            media = client.media_upload(product.image.path)
            media_ids.append(media.media_id)

        client.update_status(status=text, media_ids=media_ids if media_ids else None)
        print(f"Product tweet sent: {product.name}")
    except Exception as e:
        print(f"Error tweeting product: {e}")
