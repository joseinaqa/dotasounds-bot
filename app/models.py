from django.db import models


class Audio(models.Model):
    title = models.CharField(max_length=256)
    src = models.CharField(max_length=256)
