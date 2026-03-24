from django.contrib import admin
from django.urls import path
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('messages/', views.messages_view, name='messages'),
]