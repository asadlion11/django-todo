from django.shortcuts import render, redirect
from todo.forms import CustomUserCreationForm, LoginForm, TodoForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Todo
from django.http import HttpResponse
from django.db import models
from django.core.paginator import Paginator

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
@login_required  # you can't access the views's urls withot login, means only logged user can access the page(url)
def dashboard(request):
    all_todos = Todo.objects.filter(created_user=request.user)
    total_todos = all_todos.count()
    done_todos = all_todos.filter(status='DONE').count()
    in_progress_todos = all_todos.filter(status='IN_PROGRESS').count()
    undone_todos = all_todos.filter(status='TODO').count()
    waiting_todos = in_progress_todos + undone_todos
    
    context = {
        "total_todos": total_todos,
        "done_todos": done_todos,
        "in_progress_todos": in_progress_todos,
        "undone_todos": undone_todos,
        "waiting_todos": waiting_todos
    }
    return render(request, 'todo/dashboard.html',context)


@login_required
def todos(request):
    # Get all todos for the user
    todos = Todo.objects.filter(created_user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        todos = todos.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(status__icontains=search_query) |
            models.Q(id__icontains=search_query)
        )
    
    # Status filtering
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        todos = todos.filter(status=status_filter)
    
    # Sorting (default to ID ascending)
    sort_by = request.GET.get('sort', 'id_asc')
    if sort_by == 'id_asc':
        todos = todos.order_by('id')
    elif sort_by == 'newest':
        todos = todos.order_by('-created_at')
    elif sort_by == 'oldest':
        todos = todos.order_by('created_at')
    elif sort_by == 'a_z':
        todos = todos.order_by('title')
    elif sort_by == 'z_a':
        todos = todos.order_by('-title')
    else:
        todos = todos.order_by('id')
    
    # Pagination (10 items per page)
    paginator = Paginator(todos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "todos": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
        "sort_by": sort_by,
        "total_count": paginator.count,
    }
    return render(request, 'todo/todos.html', context)


# new todo view and its url is dashboard/new
@login_required 
def new_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False) # create a todo object but don't save it yet
            todo.created_user = request.user # associate the todo with the current user
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
    todo = get_object_or_404(Todo, id=id, created_user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.created_user = request.user
            todo.save()
            return redirect('todos')
    form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', context={"form": form})
  

# delete todo view and its url is dashboard/todo/delete/<int:id> eg: dashboard/todo/delete/1
@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, created_user=request.user)
    if request.method == 'POST':
        todo.delete()
    return redirect('todos')
