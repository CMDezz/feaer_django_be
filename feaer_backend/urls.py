from django.urls import path,include
# from feaer_backend.apis.Employee import Employee_urls
# from feaer_backend.apis.Department import Department_urls
from feaer_backend.apis.Department import Department_apis
from feaer_backend import views
urlpatterns = [
    # path('/department',include('feaer_backend.apis.Department.Department_urls')),
    path('',views.getAllDepartment),
    path('department/',views.getAllDepartment),
    path('employee/',include('feaer_backend.apis.Employee.Employee_urls'))
]