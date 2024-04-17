from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ChatMessageForm
from .models import ChatGroup, ChatMessage


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


@login_required
def group(request):
    chat_group = get_object_or_404(ChatGroup, groupName="Work")
    chat_messages = chat_group.chat_messages.all()
    form = ChatMessageForm()
    
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
    
    return render(request, 'chat/group.html', {
        "group_name": chat_group.groupName,
        "chat_messages": chat_messages,
        'form': form
    })
    
    
# Test View
def example(request):
    return