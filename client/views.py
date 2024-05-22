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
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
def home(request):
	packages = Package.objects.filter(status=2)
	return render(request, 'client/dashboard.html', {'packages': packages})

def photographerDashboard(request):
	context = {}
	return render(request, 'photographer/dashboard.html', context)
def adminDashboard(request):
    total_users = Client.objects.filter(is_client=1).count()
    total_photographers = Client.objects.filter(is_photographer=1).count()
    total_admins = Client.objects.filter(is_admin=1).count()
    completed_orders = HiringDetails.objects.filter(status=3).count()
    pending_orders = HiringDetails.objects.filter(status=1).count()
    approved_orders = HiringDetails.objects.filter(status=2).count()
    approved_packages = Package.objects.filter(status=2).count()
    pending_packages = Package.objects.filter(status=1).count()
    declined_packages = Package.objects.filter(status=3).count()

    context = {
        'total_users': total_users,
        'total_photographers': total_photographers,
        'total_admins': total_admins,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'approved_packages': approved_packages,
        'pending_packages': pending_packages,
        'declined_packages': declined_packages,
    }
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

def delete_package(request, hireIno_id):
    hire_info = get_object_or_404(HiringDetails, id=hireIno_id)

    if hire_info:
        hire_info.delete()
        messages.success(request, 'Package has been successfully cancelled.')
        return redirect('track_order')  
    
    messages.error(request, 'Invalid request method.')
    return redirect('track_order')

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
    
@login_required
def updateProfilee(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST['name']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        password = request.POST['new_password']
        if password:
            user.password = make_password(password)
            user.save()
            update_session_auth_hash(request, user)  # Prevents logout
        else:
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
            form_instance.photographer_id = package.user.id  
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