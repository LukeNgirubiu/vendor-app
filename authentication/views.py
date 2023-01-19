

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import UserSerializer,UserShowSerializer
from .models import User
from django.shortcuts import get_object_or_404


# Create your views here.
class UsersView(generics.GenericAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAdminUser,IsAuthenticated]
    def post(self,request):
        serialize= self.serializer_class(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(data={"name":serialize.data['username']},status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,user_id):
        user=get_object_or_404(User,pk=user_id)
        serialize=self.serializer_class(data=request.data,instance=user)
        if serialize.is_valid():
            serialize.save()
            return Response(data={"status":"success","email":user.email},status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        if request.data.get('email'," ")==" ":
            return Response(data={"error":"Email is required"},status=status.HTTP_400_BAD_REQUEST)
        user=get_object_or_404(User,email=request.data.email)
        serilize=self.serializer_class(instance=user)
        return Response(data=serilize.data,status=status.HTTP_200_OK)
    def delete(self,request):
        if request.data.get('email'," ")==" " or request.data.get('phone_number'," ")==" ":
            return Response(data={"error":"Email is required"},status=status.HTTP_400_BAD_REQUEST)
        user=get_object_or_404(User,email=request.data.email,phone_number=request.data.phone_number)
        resdata={"activity":'deleting user',"feedback":f"Deleted {user.username}"}
        return Response(data=resdata,status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])      
def AllUsers(request):
    users=User.objects.all()
    serialize=UserShowSerializer(users,many=True)
    return Response(data=serialize.data,status=status.HTTP_200_OK)
#


   
    

    




    

    
    


