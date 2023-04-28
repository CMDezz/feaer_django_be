from django.urls import path
from feaer_backend.apis.User import User_apis

urlpatterns = [
    path('',User_apis.getAll),
    path('createUser',User_apis.create),
    path('deleteUser',User_apis.deleteOne),
    path('editUser',User_apis.edit),
    path('signIn',User_apis.SignIn),
    path('signInAdmin',User_apis.SignInAdmin),
    path('signOut',User_apis.SignOut),

    #get thong tin user
    path('getUserInfo',User_apis.getUserInfo),

]