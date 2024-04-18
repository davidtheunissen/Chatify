from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ChatMessageForm
from .models import ChatGroup, User


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(index)
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
            return redirect(index)
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


def profile(request, username):
    users = User.objects.exclude(username=username)
        
    context = {
        "users": users,
    }
    return render(request, 'chat/profile.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect(index)
    
    other_user = User.objects.get(username=username)
    user_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    if user_chatrooms.exists():
        for chatroom in user_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)
        
    return redirect(group, chatroom.groupName)


@login_required
def group(request, group_name):
    chat_group = get_object_or_404(ChatGroup, groupName=group_name)
    chat_messages = chat_group.chat_messages.all()
    form = ChatMessageForm()
    
    # Declare other user as none
    other_user = None
    # If chat is private, find other user and store it
    if chat_group.is_private:
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    
    # If message is sent, create a HTMX partial and append it to the view
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            
            # HTMX partial information
            context = {
                'message': message,
                'user': request.user
            }
            
            return render(request, 'chat/partials/chat_message_partial.html', context)
    
    # Context information
    context = {
        "group_name": chat_group.groupName,
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
    }
    
    return render(request, 'chat/group.html', context)
    
    
# Test View
def example(request):
    return