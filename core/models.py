from django.db import models


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='carousel')

    def __str__(self):
        return self.title
