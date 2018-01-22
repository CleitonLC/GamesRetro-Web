from django.db import models


class Rating(models.Model):
    console = models.TextField()
    game_rom = models.TextField()
