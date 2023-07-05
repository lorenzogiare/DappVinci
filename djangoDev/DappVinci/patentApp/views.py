from .models import Patent, DepositInfo, Account
from .forms import LoginForm, RegistrationForm, SearchBarForm, NewPatentForm, DepositInfoForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# manages the Homepage, list of filtered patent
def homepage(request):

    if request.method == 'POST':
        patents = Patent.objects.all().order_by('-id')
        form = SearchBarForm(request.POST)

        # orders the articles
        if request.POST['patent_order'] == 'least recent':
                patents = patents.reverse()

        if form.is_valid():
                
            # filters of the articles shown
            if request.POST['search_filter'] != '':
                patents = patents.filter(title__contains=request.POST['search_filter'])

            if request.POST['owner_filter'] != 'any':
                patents = patents.filter(owner=request.POST['owner_filter'])
            
    else:
        patents = Patent.objects.all().order_by('-title')
        form = SearchBarForm()
    
    return render(request, 'patentApp/home.html', {'form':form, 'patents': patents})


# ------------ USER LOGIN, LOGOUT AND REGISTRATION ------------------------------------------------

# manages the login view
def userLogin(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            # if user exists, log in
            if user is not None :
                login(request, user)
                return redirect('/DappVinci/')
            else:
                # Return an 'invalid login' message.
                messages.error(request,'incorrect username or password')
                return redirect('/DappVinci/login/')
    else:
        form = LoginForm()
    return render(request, 'patentApp/login.html', {'form':form, 'messages':get_messages(request)})

# manages the logout action
def userLogout(request):
    logout(request)

    return redirect('/DappVinci/')

# manaes the registration view
def registration(request):
   
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = request.POST['username']

            # checks if username is already taken
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already taken')

            #if username not taken (creates user and logs in)
            else:
                user = User.objects.create_user(
                    username = username,
                    password = request.POST['password'], 
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'])

                user.save()
                account = Account.object.get(id=user.id)
                account.address = request.POST['address']
                account.save()
                login(request, user)

                return redirect('/DappVinci/')
    else:

        form = RegistrationForm()

    return render(request, 'patentApp/register.html', {'form':form, 'messages':get_messages(request)})


# ----------- READ, EDIT and FILL-OUT A PATENT ----------------------------------------------------

# manages the view of a specific patent
def readPatent(request, pk):
    patent = Patent.objects.get(pk=pk)
    context = (request.user == patent.owner) 

    return render(request, 'patentApp/readPatent.html', {'patent': patent, 'user_is_owner':context})

# manages the view to edit a patent
def editPatent(request, pk):
    pass

# manages the form for a new patent
@login_required(login_url='/DappVinci/login/')
def newPatent(request):
    if request.method == "POST":
    
        form1 = NewPatentForm(request.POST, request.FILES)
        form2 = DepositInfoForm(request.POST)

        # once the patent has been filled-in, do things...
        if form1.is_valid() and form2.is_valid():

            # fill-out fields of the patent
            patent_content = form1.save(commit=False) 
            deposit_info = form2.save(commit=False)
            count =  Patent.objects.all().count() + 1

            patent_content_dict = {
                'hash' : '',
                'title' : patent_content.title,
                'sector' : patent_content.sector,
                'introduction' : patent_content.introduction,
                'description': patent_content.description, 
                'claims' : patent_content.claims,
                'image' : patent_content.image, 
                'depositInfo' : {
                    'currentAssignee' : deposit_info.currentAssignee,
                    'applicationDate' : timezone.now(),
                    'inventors' : deposit_info.inventors,
                    '_id': count
                },
            '_id' : count,
            }

            # create new patent object
            new_patent = Patent.objects.create(
                title = patent_content.title,
                owner = request.user,
                content = patent_content_dict,
            )
            
        

            # save patent on the database
            patent_content.save()
            new_patent.save()

            # do your things on the blockchain

            # add hash to the patent instance

            
            return redirect('readPatent', pk=new_patent.pk)

    else:
        form1 = NewPatentForm()
        form2 = DepositInfoForm()
    return render(request, 'patentApp/new&edit.html', {'form1': form1, 'form2' : form2, 'url_now':'/new'})