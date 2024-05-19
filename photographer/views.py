# views.py

from urllib import request
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from photographer.models import Income, Package
from client.models import HiringDetails
from .forms import DebitForm, PackageForm
from .utils import update_job_status
from django.db.models import Sum
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


def received_jobs(request):
    jobDetails = HiringDetails.objects.filter(photographer_id=request.user.id)
    return render(request, 'photographer/package/received_jobs.html', {'jobDetails': jobDetails})

def approve_job(request, details_id):
    return update_job_status(request, details_id, 1, 'Job accepted.')

def reject_job(request, details_id):
    return update_job_status(request, details_id, 2, 'Job rejected.')

def completed_job(request, details_id):
    details = get_object_or_404(HiringDetails, id=details_id)

    if request.method == 'POST':
        form = DebitForm(request.POST)
        if form.is_valid():
            credit = form.cleaned_data['credit']
            debit = form.cleaned_data['debit']
            profit = credit - debit
            
            # Create an Income entry
            Income.objects.create(
                photographer=request.user,
                package=details.package,
                credit=credit,
                debit=debit,
                profit=profit,
                transaction_type='credit'
            )
            
            # Update the hiring status
            details.status = 3
            details.save()

            messages.success(request, 'Job completed successfully.')
            return redirect('received_jobs')
    else:
        form = DebitForm(initial={'credit': details.package.price})

    return render(request, 'photographer/package/completed_job.html', {'form': form, 'details': details})
def accounts_info(request):
    income = Income.objects.filter(photographer_id=request.user.id)
    total_credit = income.aggregate(Sum('credit'))['credit__sum'] or 0
    total_debit = income.aggregate(Sum('debit'))['debit__sum'] or 0
    total_profit = income.aggregate(Sum('profit'))['profit__sum'] or 0

    context = {
        'total_credit': total_credit,
        'total_debit': total_debit,
        'total_profit': total_profit,
    }
    return render(request, 'photographer/incomes.html', context)
