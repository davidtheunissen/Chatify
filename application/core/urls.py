from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')), #Path to chat app
    path('chat/', include('django.contrib.auth.urls')), # Path to Django's built-in authentication system
]
