from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import os


def recipe_image_file_path(instance,filename):
    ext=os.path.splitext(filename)[1]
    filename=f'{uuid.uuid4()}{ext}'
    # print(os.path.join('uploads','recipe',filename))
    return os.path.join('uploads','products',filename)


class Category(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField()

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=120)
    description=models.TextField(null=True)
    other_product_details=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=15,decimal_places=2,default=99.99)
    color=models.CharField(max_length=20,default='white')
    image=models.ImageField(null=True,upload_to=recipe_image_file_path)

class Comment(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    content=models.TextField()
    created_at = models.DateTimeField(default=timezone.now)   
    reply_to=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    
    
    


    
class Order(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    total_price=models.DecimalField(max_digits=15,decimal_places=2,default=99.99)


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity=models.IntegerField()