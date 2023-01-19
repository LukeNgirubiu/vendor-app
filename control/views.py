from django.shortcuts import get_object_or_404,get_list_or_404
from .serializers import CategorySerialize
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import Category
from sellers.models import Sales,SalesProduct
from sellers.serializers import ShowSalesSerialize,SalesProductSerialize
class CategoryView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    serializer_class=CategorySerialize
    def post(self,request):
        serialize=self.serializer_class(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(data={"succes":f"Added {serialize.data['name']}"},status=status.HTTP_201_CREATED)
    def put(self,request):
        category=get_object_or_404(Category,name=request.data['name'])
        serialize=self.serializer_class(data=request.data,instance=category)
        if serialize.is_valid():
            serialize.save()
        return Response(data={"succes":f"Updated {serialize.data['name']}"},status=status.HTTP_202_ACCEPTED)
    def get(self,request):
        category=get_object_or_404(Category,name=request.data['name'])
        serialize=self.serializer_class(instance=category)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
   
    def delete(self,request):
        if request.data.get('name'," ")==" ":
            return Response(data={"error":"Category name is required"},status=status.HTTP_400_BAD_REQUEST)
        category=get_object_or_404(Category,name=request.data['name'])
        category.delete()
        Response(data={"status":"deleted","message":f"deleted {category.name}"},status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])      
def allCategories(request):
    serialize=CategorySerialize(Category.objects.all(),many=True)
    return Response(data=serialize.data,status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def SalesView(request):
      serialize=ShowSalesSerialize(Sales.objects.all(),many=True)
      return Response(data=serialize.data,status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def salesProducts(request,id):
    sales=Sales.objects.filter(id=id)
    if sales.exists():
        sales=get_list_or_404(SalesProduct,sale__id=id)
        serialize=SalesProductSerialize(sales,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)  
    else:
        return Response(data={'message':"This sale don't exist"},status=status.HTTP_404_NOT_FOUND)


    