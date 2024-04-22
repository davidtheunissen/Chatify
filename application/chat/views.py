from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ChatMessageForm
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
    rooms = Chatroom.objects.filter(is_private=False)
        
    context = {
        "users": users,
        "rooms": rooms
    }
    return render(request, 'chat/profile.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect(index)
    
    other_user = User.objects.get(username=username)
    user_chatrooms = request.user.chat_rooms.filter(is_private=True)
    
    if user_chatrooms.exists():
        for chat_room in user_chatrooms:
            if other_user in chat_room.members.all():
                chat_room = chat_room
                break
            else:
                chat_room = Chatroom.objects.create(is_private=True)
                chat_room.members.add(other_user, request.user)
    else:
        chat_room = Chatroom.objects.create(is_private=True)
        chat_room.members.add(other_user, request.user)
        
    return redirect(chatroom, chat_room.name)


@login_required
def chatroom(request, room_name):
    chat_room = get_object_or_404(Chatroom, name=room_name)
    chat_messages = chat_room.chat_messages.all()
    form = ChatMessageForm()
    
    # Declare other user as none
    other_user = None
    # If chat is private, find other user and store it
    if chat_room.is_private:
        for member in chat_room.members.all():
            if member != request.user:
                other_user = member
                break
    
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
        "room_name": chat_room.name,
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
    }
    
    return render(request, 'chat/chatroom.html', context)
    

@login_required
def create_group(request):
    if request.method == "POST":
        group_name = request.POST['group-name']
        members = request.POST.getlist('member-select')
        
        print(group_name) # DEBUG
        print(members) # DEBUG
        
        chat_group = Chatroom(name=group_name)
        chat_group.save()
        chat_group.members.set(members)
        return redirect(chatroom, chat_group.name)
    else:
        username = request.user.username
        return redirect(profile, username)


# Test View
def example(request):
    return