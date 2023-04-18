from django.urls import path
from feaer_backend.apis.Employee.Employee_apis import getAllEmployee

urlpatterns = [
    path('/',getAllEmployee),
]