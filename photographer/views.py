# views.py

from urllib import request
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from photographer.models import Package
from .forms import PackageForm

def PackageAddPage(request):
    context = {}
     
    form = PackageForm()
    context['form'] = form
    return render(request, 'photographer/package/add_packages.html', context)

def phototGrapherViewProfile(request):
    context={}
    return render(request, 'photographer/profile.html', context)


@login_required
def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.user_id = request.user.id
            package.save()
            messages.success(request, 'Package added successfully.')
            return redirect('view_packages')
    else:
        form = PackageForm()

    return render(request, 'photographer/package/add_packages.html', {'form': form})

def view_packages(request):
    packages = Package.objects.filter(user_id=request.user.id)
    return render(request, 'photographer/package/view_packages.html', {'packages': packages})

def edit_package(request, pk):
    # Retrieve the package object from the database
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = PackageForm(request.POST, request.FILES, instance=package)
        
        if form.is_valid():
            form.save()
            return redirect('view_packages') 
    else:

        form = PackageForm(instance=package)
    
    return render(request, 'photographer/package/edit_package.html', {'form': form, 'package': package})

def delete_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'package deleted successfully.')
        return redirect('view_packages')  
    
    return render(request, 'photographer/package/view_packages.html', {'package': package})