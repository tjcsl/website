import logging

import requests
from django.contrib.auth.models import AbstractUser
from django.db import models
from social_django.utils import load_strategy

logger = logging.getLogger(__name__)

# Create your models here.


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=105)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    @property
    def short_name(self):
        return self.username

    def api_request(self, url, params: dict = None, refresh=True):
        if params is None:
            params = {}

        social_auth = self.get_social_auth()
        params.update({"format": "json"})
        params.update({"access_token": social_auth.access_token})
        request = requests.get("https://ion.tjhsst.edu/api/{}".format(url), params=params)
        if request.status_code == 401:
            if refresh:
                try:
                    self.get_social_auth().refresh_token(load_strategy())
                except Exception as exception:  # pylint: disable=broad-except
                    logger.exception(str(exception))
                return self.api_request(url, params, False)
            else:
                logger.error("Ion API Request Failure: %d %d", request.status_code, request.json())
        return request.json()

    def get_social_auth(self):
        return self.social_auth.get(provider="ion")
