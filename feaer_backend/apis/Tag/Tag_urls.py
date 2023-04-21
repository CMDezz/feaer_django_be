from django.urls import path
from feaer_backend.apis.Tag import Tag_apis

urlpatterns = [
    path('',Tag_apis.getAll),
    path('createNewTag',Tag_apis.create),
    path('deleteTag',Tag_apis.deleteOne),
    path('editTag',Tag_apis.edit),
]