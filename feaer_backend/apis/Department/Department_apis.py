from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from feaer_backend.models import Departments
from feaer_backend.serializers import DepartmentSerializer

@csrf_exempt
def getAllDepartment(req,id=0):
    departments = Departments.objects.all()
    departments_serializer = DepartmentSerializer(departments,many=True)
    return JsonResponse(departments_serializer.data,safe=False)

@csrf_exempt
def createDepartment(req,id=0):
    departments_data = JSONParser().parse(req)
    departments_serializer = DepartmentSerializer(data=departments_data)
    print('departments_serializer ',departments_serializer)
    if (departments_serializer.is_valid()):
        departments_serializer.save()
        return JsonResponse('Added succesfully',safe=False)
    return JsonResponse('Failed to add',safe=False)
