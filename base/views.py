from django.shortcuts import render, redirect

from .models import Task, User
from .forms import TaskForm, UserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db.models import Q

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('list-task')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list-task')
        else:
            messages.error(request, "User Not Found")

    context = {}
    return render(request, 'base/login.html', context)

def registerUser(request):
    form = UserForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('list-task')
        else:
            messages.error(request, "An Error occured in Registration Process")


    context = {'form':form}
    return render(request, 'base/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login') # adding decorators | only users can be access the index.html
def listTask(request):
    tasks = Task.objects.filter(user=request.user)

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tasks = tasks.filter(
        Q(title__icontains = q)
    )
    count = tasks.filter(
        Q(completed=False)
    ).count()


    context = {'tasks': tasks, 'q':q, 'count':count}
    return render(request, 'base/index.html', context)

@login_required(login_url='login') # adding decorators | only users can be access the create-task.html
def createTask(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            # adding 'user' to the form manualy | well the form only collect the title, description, completed data
            form.instance.user = request.user
            form.save()

        return redirect('list-task')
    context = {'form':form}
    return render(request, 'base/create-task.html', context)

@login_required(login_url='login') # adding decorators | only users can be access the update-task.html
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
        return redirect('list-task')

    context = {'form':form}
    return render(request, 'base/update-task.html', context)


@login_required(login_url='login') # adding decorators | only users can be access the delete-task.html
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('list-task')
    context = {'task':task}
    return render(request, 'base/delete-task.html', context)