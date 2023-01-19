from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField
class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=20)
    class Meta:
        model=User
        fields=['username','email','phone_number','password']
    def validate(self, attrs):
        user_exist=User.objects.filter(email=attrs['email'],phone_number=attrs['phone_number']).exists()
        if user_exist:
            raise serializers.ValidationError(detail="This user already exist")
        return super().validate(attrs)
    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        print(f"User email {user.email}")
        print(f"User number {user.phone_number}")
        print(f"User name {user.username}")
        user.set_password(validated_data['password'])
        user.save()
        return user
class UserShowSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','phone_number']

