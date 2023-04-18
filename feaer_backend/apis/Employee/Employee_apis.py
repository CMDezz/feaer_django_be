from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from feaer_backend.models import Employees

def getAllEmployee(req,res,next):
    return