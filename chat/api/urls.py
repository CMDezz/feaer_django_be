from django.urls import path
from chat import views
from .views import (
    getThreads,
    createThreads
)
urlpatterns = [
    path("adminChat/", views.index, name="index"),
    path("adminChat/<str:room_name>/", views.room, name="room"),
    path('',getThreads),
    path('createThreads',createThreads),
]