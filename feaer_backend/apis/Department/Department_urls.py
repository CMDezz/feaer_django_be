from django.urls import path
from feaer_backend.apis.Department.Department_apis import getAllDepartment

urlpatterns = [
    path('/',getAllDepartment),
]