from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
     user =models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
     name=models.CharField(max_length=200,null=True)
     email=models.CharField(max_length=200,null=True)

     def __str__(self):
          return self.name

     
class Product(models.Model):
     category=models.CharField(max_length=200,default='Default Category',null=True)
     brand=models.CharField(max_length=200,null=True)
     price=models.FloatField()
     description=models.TextField()
     image=models.ImageField(null=True,blank=True)
     image1=models.ImageField(null=True,blank=True,default='default.jpg')
     image2=models.ImageField(null=True,blank=True,default='default.jpg')
     image3=models.ImageField(null=True,blank=True,default='default.jpg')

  
     def __str__(self):
          return self.category
     
     @property
     def imageURL(self):
          try:
               url=self.image.url
          except:
               url=''
          return url

class Order(models.Model):
     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
     date_ordered=models.DateTimeField(auto_now_add=True)
     complete=models.BooleanField(default=False,blank=False,null=True)
     transaction_id=models.CharField(max_length=100,null=True)

     def __str__(self):
          return str(self.id)
     
     def shipping(self):
          shipping=False
          orderItems=self.orderitem_set.all()
          for i in orderItems:
               if i.product.digital ==False:
                    shipping=True
          return shipping     
     @property
     def get_cart_total(self):
          orderitems=self.orderitem_set.all()
          total=sum([item.get_total for item in orderitems])
          return total
     
     @property
     def get_cart_items(self):
          orderitems=self.orderitem_set.all()
          total=sum([item.quantity for item in orderitems])
          return total
     
class OrderItem(models.Model):
     product=models.ForeignKey(Product, on_delete=models.SET_NULL , null=True,blank=True)
     order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
     quantity=models.IntegerField(default=0,null=True, blank=True )
     date_added=models.DateTimeField(auto_now_add=True)

     @property
     def get_total(self):
          total=self.product.price * self.quantity
          return total

class ShippingAddress(models.Model):
     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
     order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
     address=models.CharField(max_length=200,null=True)
     city=models.CharField(max_length=200,null=True)
     state=models.CharField(max_length=200,null=True)
     zipcode=models.CharField(max_length=200,null=True)
     date_added=models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.address


class Review(models.Model):
    product = models.ForeignKey("Product", related_name="reviews",on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)
    comment_body=models.TextField()