from django.contrib import admin
from .models import Product,Category,Collection,Tag,Sex,Discount,User,Contact
from bson import ObjectId
import itertools
from .common.Fields import MyJSONField
import json
from jsoneditor.forms import JSONEditor

# Register your models here.

# admin.site.register(Category)
admin.site.register(Collection)
# admin.site.register(Contact)
admin.site.register(Tag)
admin.site.register(Discount)

@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = ('Name','_id')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('Name','Subject','_id')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Name','_id')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        MyJSONField: {'widget': JSONEditor(attrs={'style': 'width: 620px;'})}
    }
    def get_form(self, request, obj=None, **kwargs):
        data = request.POST.copy()
        print('data ne ',data)
        if request.POST:
            ForeignKeyToObjectId('Sex',data)
            ForeignKeyToObjectId('Discount',data)
            ArrayReferenceFieldToObjectId('Category',data)
            ArrayReferenceFieldToObjectId('Tag',data)
            ArrayReferenceFieldToObjectId('Collection',data)
            print('data ',data)
            # StringToJSONField('SizeAndStock',data)
            request.POST = data
        return super().get_form(request, obj=obj, **kwargs)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        data = request.POST.copy()
        if request.POST:
            # ArrayReferenceFieldToObjectId('Order',data)
            # StringToJSONField('SizeAndStock',data)
            request.POST = data
        return super().get_form(request, obj=obj, **kwargs)


def ForeignKeyToObjectId (name,data):
    if (name in data and data[name]):
        data[name] = ObjectId(data[name])

def ArrayReferenceFieldToObjectId (name,data):
    if (name in data and data[name]):
        _cloneList = data.getlist(name)
        data.setlist(name,list(map(lambda field: ObjectId(field),_cloneList)))

def StringToJSONField(name,data):
    if (name in data and data[name]):
        print(' -------data[name]' ,data[name])
        print(' -------data[name]' ,type(data[name]))
        data[name] = str(json.loads(data[name]))
