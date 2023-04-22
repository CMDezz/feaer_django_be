from djongo import models
from django import forms
from django.db import models as modelDjango
import uuid
from .common.Fields import MyJSONField
# from bson import ObjectId

# class DjongoModelChoiceField(forms.ModelChoiceField):
#     def to_python(self, value):
#         return self.queryset.get(_id=ObjectId(value))

# Create your models here.

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
    Sex = models.ForeignKey('Sex',on_delete=models.CASCADE,null=False, blank=False,db_column='Sex')
    Category = models.ArrayReferenceField(Category,on_delete=models.CASCADE,db_column='Category')
    Collection = models.ArrayReferenceField(Collection,on_delete=models.CASCADE,db_column='Collection')
    SizeAndStock = MyJSONField(default={},null=True,blank=True)
    Image=MyJSONField(default=[],null=True,blank=True)
    ImageDetail=MyJSONField(default=[],null=True,blank=True)
    Discount=models.ForeignKey('Discount',on_delete=models.CASCADE,null=True, blank=True,db_column='Discount')
    TotalSold=models.IntegerField(default=0)
    Tag = models.ArrayReferenceField(Tag,on_delete=models.CASCADE,null=True, blank=True,db_column='Tag')
    updatedAt = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = 'updatedAt'

    def __str__(self):
        return self.Name
