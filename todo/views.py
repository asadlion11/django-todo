from django.shortcuts import render, redirect
from todo.forms import CustomUserCreationForm, LoginForm, TodoForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Todo
from django.http import HttpResponse
from django.db import models
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.db.models import Count, Q
from datetime import datetime, timedelta

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
    # Overall todos (owned + shared)
    overall_todos = Todo.objects.filter(
        models.Q(created_user=request.user) | 
        models.Q(shared_with=request.user)
    ).distinct()
    
    # Owned todos only
    owned_todos = Todo.objects.filter(created_user=request.user)
    
    # Shared todos only
    shared_todos = Todo.objects.filter(shared_with=request.user).exclude(created_user=request.user)
    
    # Overall statistics
    overall_total = overall_todos.count()
    overall_done = overall_todos.filter(status='DONE').count()
    overall_in_progress = overall_todos.filter(status='IN_PROGRESS').count()
    overall_todo = overall_todos.filter(status='TODO').count()
    
    # Owned statistics
    owned_total = owned_todos.count()
    owned_done = owned_todos.filter(status='DONE').count()
    owned_in_progress = owned_todos.filter(status='IN_PROGRESS').count()
    owned_todo = owned_todos.filter(status='TODO').count()
    
    # Shared statistics
    shared_total = shared_todos.count()
    shared_done = shared_todos.filter(status='DONE').count()
    shared_in_progress = shared_todos.filter(status='IN_PROGRESS').count()
    shared_todo = shared_todos.filter(status='TODO').count()
    
    context = {
        # Overall stats
        "overall_total": overall_total,
        "overall_done": overall_done,
        "overall_in_progress": overall_in_progress,
        "overall_todo": overall_todo,
        
        # Owned stats
        "owned_total": owned_total,
        "owned_done": owned_done,
        "owned_in_progress": owned_in_progress,
        "owned_todo": owned_todo,
        
        # Shared stats
        "shared_total": shared_total,
        "shared_done": shared_done,
        "shared_in_progress": shared_in_progress,
        "shared_todo": shared_todo,
        
        # For progress calculation
        "waiting_todos": overall_in_progress + overall_todo
    }
    return render(request, 'todo/dashboard.html',context)


@login_required
def todos(request):
    # Get all todos for the user
    # todos = Todo.objects.filter(created_user=request.user)
    
    # Get both owned todos and shared todos
    # models.Q(...) - Creates complex queries with OR conditions
    todos = Todo.objects.filter(
        models.Q(created_user=request.user) | # Todos I created
        models.Q(shared_with=request.user)  # Todos shared with me
    ).distinct() # .distinct() - Removes duplicates (in case a user shares a todo with themselves)
    
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
    shared_filter = request.GET.get('shared', 'all')
    if shared_filter == 'owned':
        todos = todos.filter(created_user=request.user)
    elif shared_filter == 'shared':
        todos = todos.filter(shared_with=request.user).exclude(created_user=request.user)
    if status_filter != 'all':
        todos = todos.filter(status=status_filter)

    
    # Sorting (default to newest first)
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        todos = todos.order_by('-created_at')
    elif sort_by == 'id_asc':
        todos = todos.order_by('id')
    elif sort_by == 'oldest':
        todos = todos.order_by('created_at')
    elif sort_by == 'a_z':
        todos = todos.order_by('title')
    elif sort_by == 'z_a':
        todos = todos.order_by('-title')
    else:
        todos = todos.order_by('-created_at')
    
    # Pagination (10 items per page)
    paginator = Paginator(todos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "todos": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
        "shared_filter": shared_filter,
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
            todo.save() # save the todo object first
            
            # Handle optional sharing
            share_with_username = request.POST.get('share_with_username', '').strip()
            if share_with_username:
                try:
                    from .models import User
                    user_to_share_with = User.objects.get(username=share_with_username)
                    if user_to_share_with != request.user:
                        todo.shared_with.add(user_to_share_with)
                        # You could add a success message here if needed
                except User.DoesNotExist:
                    # You could add an error message here if needed
                    pass
            
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
    # Get todo that user owns OR is shared with them
    todo = get_object_or_404(
        Todo.objects.filter(
            models.Q(created_user=request.user) | 
            models.Q(shared_with=request.user)
        ), 
        id=id
    )
    
    # Check if user is the owner or has shared access
    is_owner = todo.created_user == request.user
    is_shared_user = todo.shared_with.filter(id=request.user.id).exists() and not is_owner
    
    # Create status-only form for shared users
    from django import forms
    class StatusOnlyForm(forms.ModelForm):
        class Meta:
            model = Todo
            fields = ['status']
            widgets = {
                'status': forms.Select(attrs={
                    'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-[#F59E0B] focus:outline-none transition-colors cursor-pointer bg-white text-gray-900'
                })
            }
    
    if request.method == 'POST':
        if is_owner:
            # Owner can update everything
            form = TodoForm(request.POST, instance=todo)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.created_user = request.user
                todo.save()
                return redirect('todos')
        elif is_shared_user:
            # Shared user can only update status
            form = StatusOnlyForm(request.POST, instance=todo)
            if form.is_valid():
                form.save()
                return redirect('todos')
    
    # Create form based on user permissions
    if is_owner:
        form = TodoForm(instance=todo)
    else:
        # For shared users, create a form with only status field
        form = StatusOnlyForm(instance=todo)
    
    context = {
        "form": form,
        "is_owner": is_owner,
        "is_shared_user": is_shared_user,
        "todo": todo
    }
    return render(request, 'todo/todo_form.html', context)
  

# delete todo view and its url is dashboard/todo/delete/<int:id> eg: dashboard/todo/delete/1
@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, created_user=request.user)
    if request.method == 'POST':
        todo.delete()
    return redirect('todos')

# share todo view - allows sharing todos with other registered users
@login_required
def share_todo(request, id):
    import json
    from django.http import JsonResponse
    from .models import User
    
    # Only allow POST requests
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'})
    
    # Get the todo (only owner can share)
    todo = get_object_or_404(Todo, id=id, created_user=request.user)
    
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        
        if not username:
            return JsonResponse({'success': False, 'message': 'Username is required'})
        
        # Check if user exists
        try:
            user_to_share_with = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': f'User "{username}" not found. Please check the username.'})
        
        # Check if user is trying to share with themselves
        if user_to_share_with == request.user:
            return JsonResponse({'success': False, 'message': 'You cannot share a todo with yourself.'})
        
        # Check if already shared with this user
        if todo.shared_with.filter(id=user_to_share_with.id).exists():
            return JsonResponse({'success': False, 'message': f'Todo is already shared with {username}.'})
        
        # Add user to shared_with
        todo.shared_with.add(user_to_share_with)
        
        return JsonResponse({
            'success': True, 
            'message': f'Todo successfully shared with {username}!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred while sharing the todo'})

# check if user exists - for real-time validation
@login_required
def check_user(request):
    from django.http import JsonResponse
    from .models import User
    
    username = request.GET.get('username', '').strip()
    
    if not username:
        return JsonResponse({'exists': False, 'message': 'Username is required'})
    
    try:
        user = User.objects.get(username=username)
        is_self = user == request.user
        return JsonResponse({
            'exists': True,
            'is_self': is_self,
            'username': username
        })
    except User.DoesNotExist:
        return JsonResponse({
            'exists': False,
            'username': username
        })
    except Exception as e:
        return JsonResponse({'exists': False, 'message': 'An error occurred'})


# Chart views
@login_required
def chart_data(request):
    """API endpoint to provide data for charts"""
    
    # Get todos for the current user (owned + shared)
    todos = Todo.objects.filter(
        Q(created_user=request.user) | 
        Q(shared_with=request.user)
    ).distinct()
    
    # Status distribution data
    status_data = {
        'TODO': todos.filter(status='TODO').count(),
        'IN_PROGRESS': todos.filter(status='IN_PROGRESS').count(),
        'DONE': todos.filter(status='DONE').count()
    }
    
    # Completion rate
    total_todos = todos.count()
    completed_todos = status_data['DONE']
    completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
    
    # Recent activity (last 7 days)
    recent_data = []
    for i in range(6, -1, -1):
        date = datetime.now().date() - timedelta(days=i)
        day_todos = todos.filter(
            Q(created_at__date=date) | 
            Q(updated_at__date=date)
        ).count()
        recent_data.append({
            'date': date.strftime('%a'),
            'count': day_todos
        })
    
    # Priority distribution (if you have priority field, otherwise we'll use status)
    owned_todos = todos.filter(created_user=request.user).count()
    shared_todos = todos.filter(shared_with=request.user).exclude(created_user=request.user).count()
    
    chart_data = {
        'status_distribution': status_data,
        'completion_rate': round(completion_rate, 2),
        'recent_activity': recent_data,
        'ownership_distribution': {
            'owned': owned_todos,
            'shared': shared_todos
        },
        'total_todos': total_todos,
        'completed_todos': completed_todos
    }
    
    return JsonResponse(chart_data)