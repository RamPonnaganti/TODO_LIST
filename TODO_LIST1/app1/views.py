from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import Todoform
from .models import TODO1

# class HomeView(View):
#     @login_required(login_url='login')
#     def get(self, request):
#         user = request.user
#         form = Todoform()
#         todos = TODO1.objects.filter(user=user).order_by('priority')
#         page = request.GET.get('page', 1)
#         paginator = Paginator(todos, 5)
#         try:
#             posts = paginator.page(page)
#         except PageNotAnInteger:
#             posts = paginator.page(5)
#         except EmptyPage:
#             posts = paginator.page(paginator.num_pages)
#         return render(request, 'index.html', context={'form': form, 'todos': posts})

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        form = Todoform()
        todos = TODO1.objects.filter(user=user).order_by('priority')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(todos, 5)
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(5)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        context['form'] = form
        context['todos'] = posts
        context['user'] = user
        return context


class LoginUserView(View):
    def get(self,request):
        print(request.user)
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
    def post(self, request):
        form=AuthenticationForm(data=request.POST)
        print(request.user)
        if form.is_valid():
            user=authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password1=form.cleaned_data.get('password1')
            ) 
            if user is not None:
                # messages.error(request, 'notfound')
                return render(request, 'login.html',{'form':form})
        return redirect('home')


class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)

class AddTodoView(View):
    @login_required(login_url='login')
    def post(self, request):
        user = request.user
        form = Todoform(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form})

class DeleteTodoView(View):
    def get(self, request, id):
        TODO1.objects.get(pk=id).delete()
        return redirect('home')

class ChangeTodoView(View):
    def get(self, request, id, status):
        todo = TODO1.objects.get(pk=id)
        todo.status = status
        todo.save()
        return redirect('home')

class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
