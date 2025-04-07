from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('add_product/', views.add_product, name='add_product'),
]
