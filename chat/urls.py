from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('group/<str:group_name>', views.group, name="group"),
    path('start/<str:username>', views.get_or_create_chatroom, name="start-chatroom"),
    
    
    # Test Path
    path('example/', views.example, name="example"),
]