from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
## UserCreationForm this gives us a signup form which is in-built
## AuthenticationForm gives us login form
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        if request.user.is_authenticated:
            user = request.user
            form = TODOForm()
            todos = TODO.objects.filter(user = user).order_by('priority')
            page = request.GET.get('page', 1)
            paginator = Paginator(todos, 5)
            

            
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                    posts = paginator.page(5)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
                print(posts,todos)
            return render(request,'index.html',context = {'form' : form, 'todos' : posts})

def login(request):
    if request.method == 'Get':
        form = AuthenticationForm()
        context={ ## context will send a HTML file and we can insert data
            "form" : form
        }
        return render(request,'login.html',context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context={
                "form" : form
            }
            return render(request,'login.html',context=context)

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        ## for displaying the form we need to use context
        context = { ## context will send a HTML file and we can insert data
            "form" : form
        }
        return render(request,'signup.html',context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form" : form
        }
        if form.is_valid(): # django will check if user name is present before or not and it checks if both password entered same or not
            user = form.save() ## data is stored in user
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request,'signup.html',context=context)

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
    form = TODOForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        return redirect("home")
    else:
        return render(request,'index.html',context={'form' : form})

def delete_todo(request,id):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request,id, status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')

def signout(request):
    logout(request)
    return redirect('login')