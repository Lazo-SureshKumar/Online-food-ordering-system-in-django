from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile =models.CharField(max_length=10,null=False)
    profile_pic = models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True,default='static/defult.jpg')
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Items(models.Model):
    name = models.CharField(max_length=40,null=False,blank=False)
    image = models.ImageField(upload_to='food_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    item = models.ForeignKey('Items',on_delete=models.CASCADE)
    email = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=40,null=False)
    mobile = models.CharField(max_length=10,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    order_date = models.DateField(auto_now_add=True,null=True)

class OrderedItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_id")
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.order.id)+ " q: "+ str(self.quantity) + " : " + str(self.id)

class Feedback(models.Model):
    name = models.CharField(max_length=10)
    feed_back = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name