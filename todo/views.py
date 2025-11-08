from django.shortcuts import render, redirect
from todo.forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import login, authenticate,logout
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
def dashboard(request):
    return render(request, 'todo/dashboard.html')

# new todo view and its url is dashboard/new
def new_todo(request):
    pass

# todo detail view and its url is dashboard/todo/<int:id>
def todo_detail(request, id):
    pass

# new todo view and its url is dashboard/todo/update/<int:id> eg: dashboard/todo/update/1
def update_todo(request, id):
    pass

# delete todo view and its url is dashboard/todo/delete/<int:id> eg: dashboard/todo/delete/1
def delete_todo(request, id):
    pass


