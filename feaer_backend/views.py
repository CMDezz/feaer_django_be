from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from feaer_backend.models import Departments
from feaer_backend.serializers import DepartmentSerializer

# Create your views here.
@csrf_exempt
def getAllDepartment(req,id=0):
    print('eheheheh')
    departments = Departments.objects.all()
    departments_serializer = DepartmentSerializer(departments,many=True)
    return JsonResponse(departments_serializer.data,safe=False)
