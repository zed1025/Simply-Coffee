'''
REFERENCE: https://stackoverflow.com/questions/53091688/modeling-product-orders-in-django
'''


from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

import datetime


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("id", "phone"), )


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    phone = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.CharField(max_length=500)

    def __str__(self):
        order_id = self.phone.phone+str(self.id)
        return order_id


'''
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)

    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$',  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False)

    email = models.EmailField(max_length=254)
    dob = models.DateField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    item_name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.item_name


class OrderDetail(models.Model):
    order = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date_time = models.DateTimeField()

    def __str__(self):
        return self.order.name
'''
