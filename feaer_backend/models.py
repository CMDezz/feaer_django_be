from djongo import models
from django import forms
from django.db import models as modelDjango
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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
    # dành cho đơn hàng
    Quantity=models.IntegerField(default=0)
    Size=models.CharField(max_length=5,blank=True,null=True,default='')
    class Meta:
        get_latest_by = 'updatedAt'

    def __str__(self):
        return self.Name

#User
class Order(models.Model):
    _id = models.ObjectIdField()
    UserId=models.ForeignKey('User',on_delete=models.CASCADE,null=True, blank=True,db_column='Discount')

    def __str__(self):
        return self.Name
    

class MyUserManager(BaseUserManager):
    def create_user(self, Mail, Password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not Mail:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(Mail)
        user = self.model(Mail=email, **extra_fields)
        user.set_password(Password)
        user.save(using=self._db)
        print('=====user sau khi return  ',user)
        return user

    def create_superuser(self, Mail, Password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(Mail, Password, **extra_fields)

#User
class User(AbstractBaseUser):
    _id = models.ObjectIdField()
    UserName=models.EmailField(max_length=250,blank=True,null=True,unique=True)
    Mail = models.EmailField(max_length=250,unique=True)
    Password = models.CharField(max_length=250)
    Order = models.ArrayReferenceField(Order,on_delete=models.CASCADE,null=True, blank=True,db_column='Order')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'Mail'
    REQUIRED_FIELDS = ['Password']

    objects = MyUserManager()

    def __str__(self):
        return self.Mail

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

#Contact
class Contact(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=150)
    Mail=models.EmailField(max_length=250,blank=True,null=True,unique=True)
    Subject = models.TextField()
    Desc = models.TextField()
