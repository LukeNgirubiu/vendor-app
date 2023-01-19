from django.shortcuts import get_object_or_404,get_list_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Product,Customer,Sales,SalesProduct
from control.models import Category
from authentication.serializers import UserSerializer
from authentication.models import User

@api_view(['POST'])
def signUp(request):
    serialize=UserSerializer(data=request.data)
    if serialize.is_valid():
        serialize.save()
        return Response(data={"added":f"Added {request.data['username']}"},status=status.HTTP_201_CREATED)
    return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
class ProductsView(generics.GenericAPIView):
    serializer_class=serializers.ProductSerializer
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=self.serializer_class(data=request.data)
        if data.is_valid():
            category=get_object_or_404(Category,name=data.data['categoryName'])
            product=Product.objects.create(
            category=category,
            name=data.data['name'],
            quantity=data.data['quantity'],
            unitMeasure=data.data['unitMeasure'],
            barCode=data.data['barCode'],
            buyingPrice=data.data['buyingPrice'],
            sellingPrice=data.data['sellingPrice'],
            currencyInitial=data.data['currencyInitial']
        )
            product.save()
            return Response(data={'message':f"Add {request.data['name']} successfully"},status=status.HTTP_201_CREATED)
        return Response(data=data.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,id):
        try:
            product=get_object_or_404(Product,pk=id)
            serialize=self.serializer_class(instance=product)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        except Exception as ex:
            d=str(ex)
            print(d)
            return Response(data={'message':'Failed'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def put(self,request,id):
        product=get_object_or_404(Product,pk=id)
        data=self.serializer_class(data=request.data,instance=product)
        if data.is_valid():
            data.save()
            return Response(data={'message':f"Updated {request.data['name']} successfully"},status=status.HTTP_200_OK)
        return Response(data=data.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        product.delete()
        return Response(data={'message':f"Deleted {product.name} successfully"},status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
@permission_classes([IsAuthenticated])       
def recordSale(request):
    CustomerOb={
        'fullName':request.data['fullName'],
        'phoneNumber':request.data['phoneNumber'],
        'email':request.data['email'],
        'gender':request.data['gender']
    } 
    CustSerialize=serializers.CustomerSerializer(data=CustomerOb)
    if CustSerialize.is_valid():
        customer=Customer.objects.filter(phoneNumber=request.data['phoneNumber'])
        if customer.exists()!=True:
            custom=Customer(
            fullName=CustSerialize.validated_data['fullName'],
            phoneNumber=CustSerialize.validated_data['phoneNumber'],
            email=CustSerialize.validated_data['email'],
            gender=CustSerialize.validated_data['gender']
            )
            custom.save()
        print("Getting here")
        TotalCost=0.0
        items=0
        for product in request.data['products']:
            prod=Product.objects.filter(pk=int(product['id']))
            if prod.exists():     
                TotalCost=TotalCost+float(prod[0].sellingPrice)*product['quantity']
                items=items+1
            else:
                return Response(data={"error":f"Product with id {product['id']}"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('salesType',None)!=None:
            customer=get_object_or_404(Customer,phoneNumber=request.data['phoneNumber'])
            user=get_object_or_404(User,pk=request.user.id)
            sell=Sales(
                items=items,
                salesType=request.data['salesType'],
                saleValue=TotalCost,
                soldBy=user,
                boughtBy=customer
            )
            sell.save()
            sell=Sales.objects.get(pk=1)
            for prodIt in request.data['products']:
                prod=Product.objects.get(pk=prodIt['id'])
                sale_products=SalesProduct(
                    sale=sell,
                    product=prod,
                    items=prodIt['quantity']
                )
                sale_products.save()
            return  Response(data={"message":"Sales recorded"},status=status.HTTP_201_CREATED)
        else:
             return Response(data={"error":"Provide the type of sales"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data=CustSerialize.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])  
@permission_classes([IsAuthenticated])     
def allCustomers(request):
      serialize=serializers.CustomerSerializer(Customer.objects.all(),many=True)
      return Response(data=serialize.data,status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def salesBySeller(request):
      sales=Sales.objects.filter(soldBy=request.user)
      serialize=serializers.ShowSalesSerialize(sales,many=True)
      return Response(data=serialize.data,status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def salesBySeller(request):
      sales=Sales.objects.filter(soldBy=request.user)
      serialize=serializers.ShowSalesSerialize(sales,many=True)
      return Response(data=serialize.data,status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def salesProducts(request,id):
    sales=Sales.objects.filter(id=id)
    if sales.exists():
        if sales[0].soldBy.id==request.user.id:
            sales=get_list_or_404(SalesProduct,sale__id=id)
            serialize=serializers.SalesProductSerialize(sales,many=True)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'User is not the seller'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={'message':"This sale don't exist"},status=status.HTTP_404_NOT_FOUND)
@permission_classes([IsAuthenticated]) 
@api_view(['PUT'])      
def updateCustomerDetails(request,cust_id):
    customer=get_object_or_404(Customer,pk=cust_id)
    print(f"Data is here {customer.fullName}")
    serialize=serializers.CustomerSerializerUpdate(data=request.data)
    if serialize.is_valid():
        print("Is valid")
        customer.fullName= serialize.validated_data['fullName']
        customer.email=serialize.validated_data['email']
        customer.gender=serialize.validated_data['gender']
        customer.save()
    return Response(data={'message':'Customer details updated'},status=status.HTTP_201_CREATED)
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def productSoldUpdate(request,sales_id):
    sell=Sales.objects.get(pk=sales_id)
    if sell.soldBy.id!=request.user.id:
        return Response(data={'message':'User is not the seller'},status=status.HTTP_400_BAD_REQUEST)
    TotalCost=0.0
    items=0
    for product in request.data['products']:
        prod=Product.objects.filter(pk=int(product['id']))
        if prod.exists():     
            TotalCost=TotalCost+float(prod[0].sellingPrice)*product['quantity']
            items=items+1
        else:
            return Response(data={"error":f"Product with id {product['id']}"},status=status.HTTP_400_BAD_REQUEST)
    sell.items=items
    sell.saleValue=TotalCost
    sell.save()
    for prodIt in request.data['products']:
        prod=Product.objects.get(pk=prodIt['id'])
        sale_products=SalesProduct.objects.filter(product=prod,sale=sell)
        if sale_products.exists():
            sale_products[0].items=prodIt['quantity']
            sale_products[0].save()
        if sale_products.exists()!=True:
            sale_products=SalesProduct(
                    sale=sell,
                    product=prod,
                    items=prodIt['quantity']
                )
            sale_products.save()
    return Response(data={'message':'Sales details updated appropriately'},status=status.HTTP_202_ACCEPTED)
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def clearSales(request,sales_id):
    sell=Sales.objects.get(pk=sales_id)
    if sell.soldBy.id!=request.user.id:
        return Response(data={'message':'User is not the seller'},status=status.HTTP_400_BAD_REQUEST)
    if sell.salesType=='Cash':
        return Response(data={'message':'This sales is already cleared'},status=status.HTTP_200_OK)
    sell.salesType='Cash'
    sell.save()
    return Response(data={'message':'Sales updated'},status=status.HTTP_202_ACCEPTED)
    




      


      


    

        

    