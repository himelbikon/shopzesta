from django.db import models
from PIL import Image
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    count_in_stock = models.IntegerField(default=15)
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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.email


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    qty_price = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.0)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.qty_price = self.product.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)
        self.update_total_price()

    def delete(self, *args, **kwargs):
        super(CartItem, self).delete(*args, **kwargs)
        self.update_total_price()

    def update_total_price(self):
        cart_items = CartItem.objects.filter(cart=self.cart)
        total_price = sum(
            [item.product.price * item.quantity for item in cart_items])

        cart = Cart.objects.get(pk=self.cart.id)
        cart.total_price = total_price
        cart.save()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.0)

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    address2 = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    name_on_card = models.CharField(max_length=255, null=True)
    card_number = models.CharField(max_length=255, null=True)
    expiration = models.CharField(max_length=100, null=True)
    cvv = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    qty_price = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.0)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)

        product = Product.objects.get(pk=self.product.id)
        product.count_in_stock -= self.quantity
        product.save()
