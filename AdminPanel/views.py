from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from AdminPanel.forms import PackageCategoryForm
from photographer.models import Income, Package
from .models import PackageCategory
from client.models import Client, HiringDetails
from django.db.models import Sum
def adminViewProfile(request):
    context={}
    return render(request, 'admin/profile.html', context)
def userList(request):
    users = Client.objects.filter(is_client=1)
    context = {
        'users': users
    }
    return render(request, 'admin/user_list.html', context)
def photographerList(request):
    users = Client.objects.filter(is_photographer=1)
    context = {
        'users': users
    }
    return render(request, 'admin/photographer_list.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(Client, id=user_id)

    if request.method == 'POST':
        user.name = request.POST['name']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        password = request.POST['password']
        if password:
            user.password = make_password(password)
        user.save()
        if user.is_client:
             return redirect('userList')
        else:
            return redirect('photographerList')
    context = {
        'user': user
    }
    return render(request, 'admin/edit_user.html', context)


def delete_user(request, user_id):
    user = Client.objects.get(id=user_id)
    user.delete()
    return redirect('userList')


def upload_category(request):
    if request.method == 'POST':
        form = PackageCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category uploaded successfully.')
            return redirect('upload_category')
    else:
        form = PackageCategoryForm()
    
    categories = PackageCategory.objects.all()
    return render(request, 'admin/upload_category.html', {'form': form, 'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(PackageCategory, id=category_id)

    form = PackageCategoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('upload_category')
    else:
        form = PackageCategoryForm(instance=category)
    return render(request, 'admin/edit_category.html', {'form': form})

def delete_category(request, category_id):
    categories = get_object_or_404(PackageCategory, id=category_id)
    categories.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('upload_category')

def see_package(request):
    packages = Package.objects.all()
    return render(request, 'admin/see_packages.html', {'packages': packages})
def approved_package(request, package_id):
    packages = get_object_or_404(Package, id=package_id)
    packages.status = 2
    packages.save()
    messages.success(request, 'Package approved successfully.')
    return redirect('see_package')
def decline_package(request, package_id):
    packages = get_object_or_404(Package, id=package_id)
    packages.status = 3
    packages.save()
    messages.success(request, 'Package declined successfully.')
    return redirect('see_package')

def client_spend_history(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    hiring_details = HiringDetails.objects.filter(client=client)
    
    for detail in hiring_details:
        photographer = Client.objects.filter(id=detail.photographer_id, is_photographer=True).first()
    
    total_spend = client.total_spend()
    context = {
        'client': client,
        'hiring_details': hiring_details,
        'total_spend': total_spend,
        'photographer': photographer
    }
    return render(request, 'admin/see_client_spend_history.html', context)


def photographer_info(request, photographer_id):
    photographer = get_object_or_404(Client, id=photographer_id)
    total_earnings = Income.total_income_for_photographer(photographer)
    # total_sent = Income.total_send(photographer)
    income = Income.objects.filter(photographer_id=photographer_id)
    total_sent = income.aggregate(Sum('debit'))['debit__sum'] or 0
    total_jobs_received = Income.objects.filter(photographer=photographer).count()
    
    context = {
        'photographer': photographer,
        'total_earnings': total_earnings,
        'total_jobs_received': total_jobs_received,
        'total_sent': total_sent,
    }
    return render(request, 'admin/photographer_info.html', context)


@login_required
def updateProfile(request):
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
        return redirect('adminViewProfile')
    else:
        # Pass user's information to the template
        context = {'user': request.user}
        return render(request, 'admin/profile.html', context)