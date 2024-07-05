from spotipy.cache_handler import CacheHandler
from .models import DatabaseCacheHandling, CustomUser

import logging

logger = logging.getLogger(__name__)


class DatabaseCacheHandler(CacheHandler):

    def __init__(self, user_id):
        self.user_id = user_id

    def get_cached_token(self):
        token_info = None

        try:
            user = CustomUser.objects.get(id=self.user_id)
            token_info = DatabaseCacheHandling.objects.filter(user=user).first().token

        except:
            logger.debug('Token not found in database')

        return token_info

    def save_token_to_cache(self, token_info):
        try:
            user = CustomUser.objects.get(id=self.user_id)
            DatabaseCacheHandling.objects.create(user=user, token=token_info)

        except Exception as e:
            logger.warning("Error saving token to cache: " + str(e))



