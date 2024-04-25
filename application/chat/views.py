from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import RegisterForm, ChatMessageForm, EditProfileForm
from .models import Chatroom, User


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(profile, user)
        else:
            form = AuthenticationForm()
            context = {
                "form": form,
                "message": "Invalid username and/or password, please try again"
            }
            return render(request, 'chat/login.html', context)
    else:
        form = AuthenticationForm()
        
    return render(request, 'chat/login.html', {
        "form": form,
    })


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(profile, user)
    else:
        form = RegisterForm()
    return render(request, 'chat/register.html', {
        "form": form,
        })


def logout_user(request):
    logout(request)
    return redirect(index)


def index(request):
    return render(request, 'chat/index.html')


@login_required
def profile(request, username):
    users = User.objects.exclude(username=username)
    public_rooms = Chatroom.objects.filter(is_private=False, is_group=True)
    user_groups = request.user.chat_rooms.filter(is_private=True, is_group=True)
        
    context = {
        "users": users,
        "public_rooms": public_rooms,
        "user_groups": user_groups
    }
    return render(request, 'chat/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            # Get the values from the form or use the current user's values if the fields are empty
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            email = request.POST.get('email', None)

            # If a field is empty, retain the original value
            first_name = first_name or request.user.first_name
            last_name = last_name or request.user.last_name
            email = email or request.user.email
            
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            form = EditProfileForm()
            context = {
                "form": form,
                "message": "Changes updated succesfully!"
            }
            
            return render(request, 'chat/edit_profile.html', context)
            
    form = EditProfileForm()
    context = {
        "form": form
    }
    
    return render(request, 'chat/edit_profile.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect(profile)
    
    other_user = User.objects.get(username=username)
    user_chatrooms = request.user.chat_rooms.filter(is_private=True, is_group=False)
    
    if user_chatrooms.exists():
        for user_chat_room in user_chatrooms:
            if other_user in user_chat_room.members.all():
                return redirect(chatroom, user_chat_room.name)
            
        chat_room = Chatroom.objects.create(is_private=True, title=f"{request.user}-{other_user}")
        chat_room.members.add(other_user, request.user)
    else:
        chat_room = Chatroom.objects.create(is_private=True, title=f"{request.user}-{other_user}")
        chat_room.members.add(other_user, request.user)
        
    return redirect(chatroom, chat_room.name)


@login_required
def chatroom(request, room_name):
    chat_room = get_object_or_404(Chatroom, name=room_name)
    chat_messages = chat_room.chat_messages.all()
    form = ChatMessageForm()
    
    # Declare other user as none
    other_user = None
    # If chat is private and not a group, find other user and store it
    if chat_room.is_private and not chat_room.is_group:
        for member in chat_room.members.all():
            if member != request.user:
                other_user = member
                break
            
    online_count = chat_room.usersOnline.count() - 1
    if online_count < 0:
        online_count = 0
    
    # If message is sent, create a HTMX partial and append it to the view
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_room
            message.save()
            
            # HTMX partial information
            context = {
                'message': message,
                'user': request.user
            }
            
            return render(request, 'chat/partials/chat_message_partial.html', context)
    
    # Context information
    context = {
        "room": chat_room,
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "online_count": online_count,
    }
    
    return render(request, 'chat/chatroom.html', context)
    

@login_required
def create_group(request):
    if request.method == "POST":
        group_title = request.POST['group-name']
        members = request.POST.getlist('member-select')
        members.append(request.user)
        is_private = request.POST.get('private-group', '')
        is_private = is_private == 'true'
        
        chat_group = Chatroom(
            title=group_title,
            owner=request.user,
            is_private=is_private,
            is_group=True
        )
        chat_group.save()
        chat_group.members.set(members)
        return redirect(chatroom, chat_group.name)
    else:
        username = request.user.username
        return redirect(profile, username)


# Test View
def example(request):
    return