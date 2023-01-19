from django.contrib import admin
from .models import Product,Customer,Sales,SalesProduct
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sales)
admin.site.register(SalesProduct)
# Register your models here.
