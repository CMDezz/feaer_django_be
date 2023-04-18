from django.urls import path
from feaer_backend.apis.Department import Department_apis

urlpatterns = [
    path('',Department_apis.getAllDepartment),
    path('createDepartment',Department_apis.createDepartment),
]