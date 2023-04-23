from django.urls import path
from feaer_backend.apis.Contact import Contact_apis

urlpatterns = [
    path('',Contact_apis.getAll),
    path('createNewContact',Contact_apis.create),
    path('deleteContact',Contact_apis.deleteOne),
    path('editContact',Contact_apis.edit),
]