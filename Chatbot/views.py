from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def direct_chat_view(request, receiver_username):
    receiver = User.objects.get(username=receiver_username)
    return render(request, 'chat/direct.html', {
        'receiver': receiver
    })
