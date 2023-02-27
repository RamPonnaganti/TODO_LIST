from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Create your views here.
class UserRegistration(FormView):
    template_name='registration/register.html'
    form_class=UserCreationForm
    # redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
            return super(UserRegistration, self).form_valid(form)
    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect('tasks')
    #     return super(UserRegistration, self).get(*args, **kwargs)



class UserLogin(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('tasks')
        