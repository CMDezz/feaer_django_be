# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# # Create your views here.
# from chat.models import Thread


# def messages_page(request):
#     threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
#     context = {
#         'Threads': threads
#     }
#     return render(request, 'messages.html', context)

# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})