from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False,unique=True)
    description=models.CharField(max_length=400,null=False,blank=False)
    def __str__(self) :
        return f"<Category {self.name}>"