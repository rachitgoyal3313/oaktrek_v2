from django.urls import path
from . import views

urlpatterns = [
    path('<str:receiver_username>/', views.direct_chat_view, name='direct_chat'),
]
