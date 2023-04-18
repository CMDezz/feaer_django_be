from rest_framework import serializers
from feaer_backend.models import Departments,Employees

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Departments
        fields=('DepartmentId','DepartmentName')

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employees
        fields=('EmployeeId','EmployeetName','Department','DateOfJoining','PhotoFileName')
