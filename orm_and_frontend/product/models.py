from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProductTable(models.Model):
    CATEGORIES = ((1,'Mobile'),(2,'Clothes'),(3,'Shoes'))
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    details=models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORIES)
    is_active = models.BooleanField()
    rating = models.FloatField()
    image = models.ImageField(upload_to='Images' ,blank=True ,null=True)
    def __str__(self):
        return self.name + "added to table"
    
class  CartTable(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE, db_column= 'uid')
    pid = models.ForeignKey(ProductTable,on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField(default=1)   

class  OrderTable(models.Model):
    order_id=models.CharField(max_length=59)
    uid = models.ForeignKey(User,on_delete=models.CASCADE, db_column= 'uid')
    pid = models.ForeignKey(ProductTable,on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField()    

class CustomerDetails(models.Model):
    ADDRESS_TYPE=(('home','HOME'),('office','Office'),('other','Other'))
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    first_nam=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address_type=models.CharField(max_length=100,choices=ADDRESS_TYPE)
    full_address=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)