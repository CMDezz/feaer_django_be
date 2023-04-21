from django.urls import path
from feaer_backend.apis.Sex import Sex_apis

urlpatterns = [
    path('',Sex_apis.getAll),
    path('createNewSex',Sex_apis.create),
    path('deleteSex',Sex_apis.deleteOne),
    path('editSex',Sex_apis.edit),
]