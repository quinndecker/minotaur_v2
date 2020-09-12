from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['username']) < 2:
            errors['username'] = ("Username must be at least 2 Characters") 
        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = ("Invalid email address!")
        elif check:
            errors['reg_email'] = "Email address is already registered!"
        if len(postData['password']) <8:
            errors['password'] = 'Password must be at least 8 characters!'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Password must match!'
        return errors
    def login_val(self,postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        return errors   

class User(models.Model):
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()  

shop_types = (
    ('Visual Artist','VISUALARTIST'),
    ('Band / Musician', 'MUSIC'),
    ('Clothing', 'CLOTHING'),
    ('Accessories', 'ACCESSORIES'),
)

class ShopManager(models.Manager):
    def shop_val(self,postData):
        errors ={}
        if len(postData['shop_name']) < 1:
            errors['shop_name'] = 'Shops must have a name!'
        return errors

class Shop(models.Model):
    shop_name = models.CharField(max_length=255, null=True)
    shop_type = models.CharField(max_length=255, choices=shop_types, default='Visual Artist')
    creator = models.ForeignKey(User, related_name='shops', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ShopManager()    


class ProductManager(models.Manager):
    def product_val(self,postData):
        errors = {}
        if len(postData['product_name']) < 1:
            errors['product_name'] = 'Product must have a name!'
        if len(postData['product_price']) < 1:
            errors['product_price'] = 'Product must have a price, if free, input 0'
        return errors

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=255)
    product_pic = models.ImageField(upload_to='uploaded_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ProductManager()


class OrderManager(models.Manager):
    def order_val(self,postData):
        errors = {}
        return errors

class Order(models.Model):
    quantity_ordered = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()