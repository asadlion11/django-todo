from django.shortcuts import render, redirect
from todo.forms import CustomUserCreationForm, LoginForm, TodoForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Todo
from django.http import HttpResponse

# Create your views here.

# register user view and its url is register/ 
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    # otherwise
    form = CustomUserCreationForm()
    return render(request, 'todo/register.html', context={"form": form})

# login user view and its url is / 
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    form = LoginForm()
    return render(request, 'todo/login.html', context={"form": form})    
    

# logput user view and its url is logout/ 
def logout_user(request):
    logout(request)
    return redirect('login')

# dasboard view and its url is dashboard
@login_required # # you can't access the views's urls withot login, means only logged user can access the page(url)
def dashboard(request):
    all_todos = Todo.objects.filter(user=request.user)
    total_todos = all_todos.count()
    done_todos = all_todos.filter(is_complete=True).count()
    undone_todos = all_todos.filter(is_complete=False).count()
    
    context = {
        "total_todos": total_todos,
        "done_todos": done_todos,
        "undone_todos": undone_todos
    }
    return render(request, 'todo/dashboard.html',context)


@login_required
def todos(request):
    # get all todos of the current user 
    # todos = request.user.todo_set.all()
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/todos.html', context={"todos": todos})

# new todo view and its url is dashboard/new
@login_required 
def new_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False) # create a todo object but don't save it yet
            todo.user = request.user # associate the todo with the current user
            todo.save() # save the todo object
            return redirect('todos')
    form = TodoForm()
    return render(request, 'todo/todo_form.html', context={"form": form})

# todo detail view and its url is dashboard/todo/<int:id>
@login_required
def todo_detail(request, id):
    pass

# new todo view and its url is dashboard/todo/update/<int:id> eg: dashboard/todo/update/1
@login_required
def update_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todos')
    form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', context={"form": form})
  

# delete todo view and its url is dashboard/todo/delete/<int:id> eg: dashboard/todo/delete/1
@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    if request.method == 'POST':
        todo.delete()
    return redirect('todos')
