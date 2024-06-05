from django.db import models
from django.contrib.auth.models import User

class LinkedAccount(models.Model):
    game_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=50)
    server = models.CharField(max_length=50)
    main_server = models.CharField(max_length=50)
    temp_icon_id = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lol_account', null=True, blank=True)

    def __str__(self):
        return f"{self.game_name}#{self.tagline} ({self.server}) - Verified: {self.verified}"


class FollowSummoner(models.Model):
    game_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=50)
    server = models.CharField(max_length=50)
    main_server = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='followSummoner', null=True, blank=True)

    def __str__(self):
        return f"User:{self.user.username} {self.game_name}#{self.tagline} ({self.server})  "