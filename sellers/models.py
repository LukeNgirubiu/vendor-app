from django.db import models
from authentication.models import User
from phonenumber_field.modelfields import PhoneNumberField
from control.models import Category
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=120,blank=False)
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField()
    unitMeasure=models.CharField(max_length=50,blank=False)
    barCode=models.CharField(max_length=70,blank=True)
    buyingPrice=models.DecimalField(max_digits=10,decimal_places=3)
    sellingPrice=models.DecimalField(max_digits=10,decimal_places=3)
    currencyInitial=models.CharField(max_length=7,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Product {self.name} Price {self.sellingPrice}"
class Customer(models.Model):
    fullName=models.CharField(max_length=40)
    phoneNumber=PhoneNumberField(null=False,unique=True)
    email=models.EmailField(blank=True)
    gender=models.BooleanField()# True->Male False->female
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Full name {self.fullName}" 
class Sales(models.Model):
    SalesType=(
        ("Cash","cash"),
        ("Invoice","invoice")
    )
    items=models.IntegerField()
    salesType=models.CharField(max_length=20,blank=False, choices=SalesType,default="Cash")
    saleValue=models.DecimalField(max_digits=10,decimal_places=3)
    soldBy=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    boughtBy=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Sales {self.id}"
class SalesProduct(models.Model):
    sale=models.ForeignKey(Sales,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    items=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Bought by {self.sale.boughtBy.fullName} product {self.product.name}"






    

 