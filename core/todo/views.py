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
from todo.models import Task
# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='items'
    paginate_by=2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks=Task.objects.filter(user=self.request.user)
        count=Task.objects.filter(user=self.request.user,complete=False).count()
        # context["items"] = context["items"].filter(user=self.request.user)
        # context["count"] = context["items"].filter(complete=False).count()
        paginator = Paginator(tasks, 3)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['items'] = file_exams
        context['count']=count
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='items'
    

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','decription','complete']
    success_url=reverse_lazy('tasks')
    template_name='todo/task_add.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields='__all__'
    success_url=reverse_lazy('tasks')
    template_name='task_update.html'

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    fields='__all__'
    success_url=reverse_lazy('tasks')
    template_name='todo/task_delete.html'
