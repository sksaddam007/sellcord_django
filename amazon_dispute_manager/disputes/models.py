# disputes/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django.templatetags.static import static


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')


class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned')
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')
    date_ordered = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Delivered')

    def __str__(self):
        return f'Order {self.id} for {self.item.name}'


class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    return_reason = models.TextField()
    return_tracking = models.CharField(max_length=50)
    date_returned = models.DateTimeField()

    def __str__(self):
        return f'Return for Order {self.order.id}'


class Dispute(models.Model):
    return_order = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='disputes')
    dispute_reason = models.TextField()
    status = models.CharField(max_length=20,
                              choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')],
                              default='Pending')
    resolution_details = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Dispute for Return {self.return_order.id}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar_default.svg')
        return avatar

    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name
