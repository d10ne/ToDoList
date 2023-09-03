from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth import logout, login
from django.views.generic import ListView, DetailView, CreateView, FormView
from .models import Task, User
from .forms import TaskForm, RegisterUserForm, LoginUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import DataMixin
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# def index(request):
#     if request.user.is_authenticated:
#         tasks = Task.objects.filter(user_id=request.user)
#         return render(request, 'todolist/index.html', {'title': 'Список заданий', 'tasks': tasks})
#     else:
#         return render(request, 'todolist/register.html')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todolist/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user_id=self.request.user)

        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('home')
    template_name = 'todolist/add.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(TaskCreate, self).form_valid(form)

# def add_task(request):
#     error = ''
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             error = 'Неверная форма'
#     else:
#         form = TaskForm()
#
#     return render(request, 'todolist/add.html', {'form': form, 'error': error})


# def delete_task(request, pk):
#     tasks = Task.objects.all()
#     task = tasks.get(id=pk)
#     task.delete()
#     return render(request, 'todolist/index.html', {'title': 'Список заданий', 'tasks': tasks})

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('home')
    template_name = 'todolist/delete.html'

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user_id=owner)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'todolist/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'todolist/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')