from django.db import models
from PIL import Image
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    details = models.TextField()

    image1 = models.ImageField(upload_to='product/')
    image2 = models.ImageField(upload_to='product/')
    image3 = models.ImageField(upload_to='product/')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        self.resize(self.image1)
        self.resize(self.image2)
        self.resize(self.image3)

    def resize(self, image):
        img = Image.open(image.path)
        img = img.resize((750, 750))
        img.save(image.path)
