from django.urls import path
from feaer_backend.apis.Collection import Collection_apis

urlpatterns = [
    path('',Collection_apis.getAll),
    path('createNewCollection',Collection_apis.create),
    path('deleteCollection',Collection_apis.deleteOne),
    path('editCollection',Collection_apis.edit),
]