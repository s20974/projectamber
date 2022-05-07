from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class MainProductsCategorie(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class ProductsSubCategorie(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(MainProductsCategorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductsSubCategorie, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Description", max_length=9000)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class JointProduct(Product):
    joined = models.ManyToManyField(User, related_name = 'joined')
    partners = models.IntegerField(default=2, verbose_name="Макс. участников")

    def __str__(self):
        return self.name
    


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image/', blank=False)
    main_photo = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + "; Owner: " + self.product.user.objects.get(id)
    
    def save(self):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = 'product_images/%d/%d' % (User.objects.get(id=product.user.id), self.name + self.id)
        super(ProductImages, self).save()
