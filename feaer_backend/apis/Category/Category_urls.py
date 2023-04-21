from django.urls import path
from feaer_backend.apis.Category import Category_apis

urlpatterns = [
    path('',Category_apis.getAll),
    path('createNewCategory',Category_apis.create),
    path('deleteCategory',Category_apis.deleteOne),
    path('editCategory',Category_apis.edit),
]