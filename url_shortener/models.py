from django.db import models


class Url(models.Model):
    counter = models.PositiveIntegerField(default=0)
    full_url = models.CharField(max_length=255)
    shortened_url = models.CharField(max_length=6, unique=True)
    creator_ip = models.CharField(max_length=15, default=None)  # ipv6?
    last_redirect_datetime = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f'{self.full_url} -> {self.shortened_url}; created by: {self.creator_ip}'


