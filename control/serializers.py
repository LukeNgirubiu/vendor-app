from rest_framework import serializers
from .models import Category
from phonenumber_field.serializerfields import PhoneNumberField
class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['name','description']
    def validate(self, attrs):
        categoryNameExists=Category.objects.filter(name=attrs['name']).exists()
        if categoryNameExists is True:
            serializers.ValidationError(detail="This category exists already")
        return super().validate(attrs)
    def create(self, validated_data):
        category=Category.objects.create(
            name=validated_data['name'],
            description=validated_data['description']
        )
        category.save()
        return category