from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views

def redirigir_a_login(request):
    return redirect('login')

urlpatterns = [
     path('', redirigir_a_login),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro, name='registro'),
   
]
