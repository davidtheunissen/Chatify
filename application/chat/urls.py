from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('room/<str:room_name>', views.chatroom, name="chatroom"),
    path('start/<str:username>', views.get_or_create_chatroom, name="start-chatroom"),
    path('create_group/', views.create_group, name="create_group"),
    
    # Test Path
    path('example/', views.example, name="example"),
]