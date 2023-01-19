from rest_framework import serializers
from .models import Product,Customer,Sales,SalesProduct
from phonenumber_field.serializerfields import PhoneNumberField
from authentication.serializers import UserSerializer
class ProductSerializer(serializers.ModelSerializer):
    categoryName=serializers.CharField()
    class Meta:
        model=Product
        fields=['name','categoryName','quantity','unitMeasure','barCode','buyingPrice','sellingPrice','currencyInitial']
    def validate(self, attrs):
        return super().validate(attrs)
   
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['fullName','phoneNumber','email','gender']
    def validate(self, attrs):
        return super().validate(attrs)
class CustomerSerializerUpdate(serializers.Serializer):
      fullName=serializers.CharField()
      phoneNumber=PhoneNumberField()
      email=serializers.EmailField()
      gender=serializers.BooleanField()
     
class SalesSerialize(serializers.ModelSerializer):
    items=serializers.IntegerField()
    saleValue=serializers.DecimalField(max_digits=10,decimal_places=3)
    def validate(self, attrs):
        return super().validate(attrs)
class ShowSalesSerialize(serializers.ModelSerializer):
    boughtBy=CustomerSerializer()
    class Meta:
        model=Sales
        #Foreign key should be as per the model
        fields=['boughtBy','items','saleValue','salesType']
class ShowProductSerialize(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name','unitMeasure','buyingPrice','sellingPrice']
class SalesProductSerialize(serializers.ModelSerializer):
    product=ShowProductSerialize()
    
    class Meta:
        model=SalesProduct
        fields=['items','product']
