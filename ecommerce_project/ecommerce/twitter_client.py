# ecommerce/twitter_client.py
import logging
from io import BytesIO
import requests
import tweepy
from django.conf import settings

logger = logging.getLogger(__name__)

def get_twitter_client():
    """Get Twitter API v2 Client"""
    if not hasattr(settings, 'TWITTER_API_KEY'):
        return None
    
    try:
        client = tweepy.Client(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_SECRET
        )
        return client
    except Exception as e:
        logger.error(f"Error creating Twitter client: {e}")
        return None


def post_tweet(status_text, image_field=None):
    """
    Post tweet using Twitter API v2
    status_text: str
    image_field: can be Django ImageFieldFile, InMemoryUploadedFile, URL string, or filesystem path
    Note: API v2 create_tweet doesn't support media in free tier, so we post text only
    """
    client = get_twitter_client()
    if not client:
        logger.info("Twitter not configured, skipping tweet")
        return False
    
    try:
        # Twitter API v2 - create_tweet (supports free tier)
        response = client.create_tweet(text=status_text[:280])  # 280 char limit
        logger.info(f"Tweet posted successfully: {status_text[:50]}...")
        return True
        
    except Exception as e:
        # Don't crash your request — log and continue
        logger.exception("Failed to post tweet: %s", e)
        return False
