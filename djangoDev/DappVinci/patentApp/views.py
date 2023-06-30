from django.shortcuts import render
from imp import reload
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages

# manages the Homepage
def homepage(request):

    if request.method == 'POST':
        ...
    else:
        ...
    return render(request, 'patentApp/home.html', {})

# manages the login view
def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            # if user exists, log in
            if user is not None :
                login(request, user)
                return redirect('DappVinci/')
            else:
                # Return an 'invalid login' message.
                messages.error(request,'incorrect username or password')
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'patentApp/login.html', {'form':form, 'messages':get_messages(request)})

