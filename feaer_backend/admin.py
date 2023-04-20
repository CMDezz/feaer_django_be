from django.contrib import admin
from .models import Departments,Employees,Product,Category,Collection,Tag,Sex,Discount
from bson import ObjectId

# Register your models here.

admin.site.register(Departments)
admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Tag)
admin.site.register(Sex)
admin.site.register(Discount)

@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.POST:
            # remember old state
            _mutable = request.POST._mutable
            # set to mutable
            request.POST._mutable = True
            # # сhange the values you want
            request.POST['Department'] = ObjectId(request.POST['Department'])
            print('eyeyey ',request.POST['Department'])
            # # set mutable flag back
            request.POST._mutable = _mutable
        return super().get_form(request, obj=obj, **kwargs)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.POST:
            # remember old state
            category = request.POST.getlist('Category')
            print('---___+++ category',category)
            print('---___+++ category',category)
            categoryObject = Category.objects.filter(pk__in=category)
            for cate in categoryObject:
                # cate._id = ObjectId() 
                print('----------- cate',cate)
            _mutable = request.POST._mutable
            # set to mutable
            request.POST._mutable = True
            # # сhange the values you want
            request.POST['Sex'] = ObjectId(request.POST['Sex'])
            request.POST['Discount'] = ObjectId(request.POST['Discount'])
            request.POST['Category'] = [ObjectId(request.POST['Category'])]
            # request.POST['Collection'] = GenerateObjectIdFromFields(request.POST['Collection'])
            # request.POST['Tag'] = GenerateObjectIdFromFields(request.POST['Tag'])
            print('++ ',request.POST)
            # # set mutable flag back
            request.POST._mutable = _mutable
        return super().get_form(request, obj=obj, **kwargs)

def GenerateObjectIdFromFields (fields):
    # return list(map(lambda x: ObjectId(x),fields))
    return ObjectId(fields)