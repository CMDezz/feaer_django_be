from djongo import models
from django import forms
from django.db import models as modelDjango
import uuid

# from bson import ObjectId

# class DjongoModelChoiceField(forms.ModelChoiceField):
#     def to_python(self, value):
#         return self.queryset.get(_id=ObjectId(value))

# Create your models here.
class Departments(models.Model):
    _id = models.ObjectIdField()
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DepartmentName = models.CharField(max_length=250)
    def __str__(self):
        return self.DepartmentName

class Employees(models.Model):
    _id = models.ObjectIdField()
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    EmployeetName = models.CharField(max_length=250)
    Department = models.ForeignKey('Departments',on_delete=models.CASCADE,db_column='departments')
    DateOfJoining = models.DateField()
    PhotoFileName = models.CharField(max_length=250)
    def __str__(self):
        return self.EmployeetName

#CATEGORY 
class Category(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=250)
    def __str__(self):
        return self.Name

#Collection 
class Collection(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=250)
    Title = models.CharField(max_length=250)
    Image = models.TextField()
    Desc = models.TextField()
    def __str__(self):
        return self.Name

#Discount 
class Discount(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=250)
    KindOfDiscount = models.CharField(max_length=250)
    Value = models.IntegerField()
    def __str__(self):
        return self.Name

#Sex 
class Sex(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=250)
    def __str__(self):
        return self.Name

#Tag 
class Tag(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=250)
    def __str__(self):
        return self.Name

#Product 
class Product(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=250)
    Desc = models.TextField()
    Price = models.IntegerField()
    FinalPrice = models.IntegerField()
    Sex = models.ForeignKey('Sex',on_delete=models.CASCADE)
    Category = models.ManyToManyField(Category)
    # Category = models.ArrayField(model_container=Category)
    # Category = models.ArrayField(model_container=Category)
    # Collection = models.ManyToManyField(Collection)
    SizeAndStock = models.JSONField(blank=True)
    Image=models.JSONField(blank=True)
    ImageDetail=models.JSONField(blank=True)
    Discount=models.ForeignKey('Discount',on_delete=models.CASCADE)
    TotalSold=models.IntegerField()
    # Tag = models.ArrayField(model_container=Tag)
    # Tag = models.ManyToManyField(Tag)
    def __str__(self):
        return self.Name
