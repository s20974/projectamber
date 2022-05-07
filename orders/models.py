from django.db import models
from authapp.models import User
from products.models import Product

# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'customer')
    seller   = models.ForeignKey(User, on_delete = models.CASCADE)
    product  = models.ForeignKey(Product, on_delete = models.CASCADE)
    details  = models.CharField("детали к заказу", max_length = 5000)
    
    def __str__(self):
        return self.customer.get_full_name() + " заказал " + self.product.name

