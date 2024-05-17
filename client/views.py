from ast import Not
from urllib import request
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User,auth
from django.urls import reverse
from client.forms import HiringForm
from photographer.models import Package
from .models import Client, HiringDetails   
from django.contrib import messages
from mysqlx import Auth
from django.contrib.auth import authenticate,logout,login as auth_login
import mysql.connector as sql 
from django.contrib.auth.decorators import login_required


def home(request):
	packages = Package.objects.all()
	return render(request, 'client/dashboard.html', {'packages': packages})
def photographerDashboard(request):
	context = {}
	return render(request, 'photographer/dashboard.html', context)
def adminDashboard(request):
	context = {}
	return render(request, 'admin/dashboard.html', context)
def blocked(request):
	context = {}
	return render(request, 'authApp/error.html', context)
def login(request):
	context = {}
	return render(request, 'authApp/login.html', context)
def signup(request):
	context = {}
	return render(request, 'authApp/signup.html', context)
def viewProfile(request):
	context = {}
	return render(request, 'authApp/profile.html', context)

def order_success_page(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    context = {'package': package}
    return render(request, 'client/order_success.html', context)


def track_order(request):
    hireInfos = HiringDetails.objects.filter(client_id=request.user.id).select_related('package')
    return render(request, 'client/track_order.html', {'hireInfos': hireInfos})

def details_page(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    context = {'package': package}  
    return render(request, 'client/view_details.html', context)

def hire_photographer_page(request, package_id):
    package =get_object_or_404(Package, id=package_id)
    context = {
        'form': HiringForm(),
        'package': package
    }
    form = HiringForm()
    context['form'] = form
    return render(request, 'client/hire_page.html', context)



def register(request):
    if request.method == 'POST':
        name=request.POST['name'] 
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        re_password=request.POST['re_password']
        user_type = request.POST.get('user_type')

        if password == re_password:
            if Client.objects.filter(email=email).exists():
                messages.info(request, 'Email Already exits')
                return redirect('register')
            if not name:
                messages.info(request, 'Please provide Name')
                return redirect('register')
            if not phone:
                messages.info(request, 'Please provide phone')
                return redirect('register')
            if not email:
                messages.info(request, 'Please provide email')
                return redirect('register')
            if not password:
                messages.info(request, 'Please provide password')
                return redirect('register')
            if not re_password:
                messages.info(request, 'Please re enter the password')
                return redirect('register')
            if not user_type:
                messages.info(request, 'Please Select a designation')
                return redirect('register')
            else:
                is_client = True if user_type == 'client' else False
                is_photographer = True if user_type == 'photographer' else False
                user= Client.objects.create_user(name=name, 
                                 email=email,phone=phone,
                                 password=password,
                                 is_client=is_client,
                                is_photographer=is_photographer)   
                user.save();
                messages.success(request, 'Registration successful. You can now login.')
                return redirect('login')
        else: 
            messages.info(request,'Password not match ' )
        return redirect('register')

    else:            
      
        return render( request,  'dashboard/signup.html')
    


def updateProfile(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')

        # Get the logged-in user
        user = request.user

        # Update user's information
        if name:
            user.name = name              
        if phone:
            user.phone = phone
        if email:
            user.email = email

        # Check if old password matches and update new password
        if old_password and new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
            else:
                messages.error(request, 'Old password does not match')
                return redirect('viewProfile')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('viewProfile')
    else:
        # Pass user's information to the template
        context = {'user': request.user}
        return render(request, 'authApp/profile.html', context)




@login_required
def hire_photographer(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        form = HiringForm(request.POST)
        if form.is_valid(): 
            form_instance = form.save(commit=False)
            form_instance.client_id = request.user.id  
            form_instance.package_id = package_id
            form_instance.save()
            messages.success(request, 'submitted successfully.')
            return redirect(reverse('order_success_page', kwargs={'package_id': package_id}))
    else:
        form = HiringForm()
    return render(request, 'client/hire_page.html', {'form': form, 'package': package})


def client_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Check if email and password are provided
        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                
                if user.is_client:
                    auth_login(request, user)
                    return redirect('dashboard')
                elif user.is_photographer:
                    auth_login(request, user)
                    return redirect('photographerDashboard')
                elif user.is_admin:
                    auth_login(request, user)
                    return redirect('adminDashboard')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Please provide both email and password')

    return render(request, 'authApp/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')