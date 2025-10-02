from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from masters.models import Employee
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

@login_required
def home(request):
    print("Home view called")
    return render(request, 'home.html')




def LoginView(request):
    print("LoginView called")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            messages.success(request, "Login successful.")
           
            
            return redirect('dashboard')  
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  
    return render(request, 'Login.html')

def logout_view(request):
    print("Logout view called")
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  



@login_required
def dashboard(request):
    try:
        employee = request.user.employee_profile 
        role_name = employee.role.role_name.lower() if employee.role else "default"

        return render(request, "dashboards/dashboard.html", {
            "employee": employee,
            "role_name": role_name,
        })

    except Employee.DoesNotExist:
        return render(request, "dashboards/dashboard.html", {"employee": None, "role_name": "default"})
