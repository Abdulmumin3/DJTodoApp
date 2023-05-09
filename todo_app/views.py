from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Task
from .forms import TaskCreateForm, LoginForm, TaskUpdateForm, SignupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.core.mail import send_mail
# Create your views here.

def landPage(request):
    return render(request, 'todo_app/landpage.html')

@login_required
def homePage(request):
    q = request.GET.get('q', None)
    if q is None or q is "":
        tasks = Task.objects.filter(user=request.user)
    elif q is not None:
        tasks = Task.objects.filter(user=request.user, title__icontains=q)
    count = Task.objects.filter(user=request.user, is_completed=False).count()
    return render(request, 'todo_app/homepage.html', {'tasks':tasks, 'count':count})

@login_required
def detailPage(request, pk):
    task = get_object_or_404(Task, id=pk)
    return render(request, 'todo_app/detail_page.html', {'task':task})

@login_required
def createPage(request):
    form = TaskCreateForm()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # form = Task(user=request.user)
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # return redirect(reverse(('todo-app:home-page')))                                                                                                                                                                                                                                                                                                           
            return redirect('todo-app:home-page')
    return render(request, 'todo_app/create_page.html', {'form':form})

@login_required
def updatePage(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task.user != request.user:
        raise Http404
    form = TaskUpdateForm(instance=task)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            # form = Task(user=request.user)
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # return redirect(reverse(('todo-app:home-page')))
            return redirect('todo-app:home-page')                                                                                                                                                                                                                                                                                                           
    return render(request, 'todo_app/update_page.html', {'form':form})

@login_required
def deletePage(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task.user != request.user:
        raise Http404
    if request.method == 'POST':
        task.delete()
        return redirect('todo-app:home-page')
    return render(request, 'todo_app/delete_page.html', {'task':task})

def loginPage(request):
    form = LoginForm()
    message = ''
    if request.user.is_authenticated:
        return redirect('todo-app:home-page')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'],)
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('land-page')
            else:
                message = 'User does not exist, check your credentials!.'
    return render(
        request, 'todo_app/login.html', {'form': form, 'message': message})

def logoutPage(request):
    logout(request)
    return redirect('login')

def signupPage(request):
    form = SignupForm()
    if request.user.is_authenticated:
        return redirect('todo-app:home-page')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password)
            # login(request, user)
            return redirect('login')
    return render(request, 'todo_app/signup.html', {'form':form})
