from django.urls import path
from feaer_backend.apis.Order import Order_apis

urlpatterns = [
    path('',Order_apis.getAll),
    path('createNewOrder',Order_apis.create),
    path('deleteOrder',Order_apis.deleteOne),
    path('editOrder',Order_apis.edit),
]