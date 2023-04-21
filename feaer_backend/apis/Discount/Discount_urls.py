from django.urls import path
from feaer_backend.apis.Discount import Discount_apis

urlpatterns = [
    path('',Discount_apis.getAll),
    path('createNewDiscount',Discount_apis.create),
    path('deleteDiscount',Discount_apis.deleteOne),
    path('editDiscount',Discount_apis.edit),
]