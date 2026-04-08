from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django import forms
# Import registration, login form
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# IMPORT LOGIN, LOGOUT FUNCTIONALITY
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

def id_admin(user):
    # Check if useris admin/superuser
    return user.is_superuser or user.is_staff
        
# REGISTRATION VIEW

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "tasks/register.html", {"form": form})

# LOGIN VIEW

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("task_list")
    else:
        form = AuthenticationForm()
    return render(request,"tasks/login.html",{"form":form})

def user_logout(request):
    logout(request)
    return redirect("login")


# TASK CREATE
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Create the task but don't upload to database
            task = form.save(commit=False)
            # Assign the task to the current user
            task.user = request.user
            # Save to the database
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# HOME VIEW
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('task_list')


 # Create your views here.
