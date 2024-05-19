# client/utils.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from client.models import HiringDetails

def update_job_status(request, details_id, status, success_message):
    approved = get_object_or_404(HiringDetails, id=details_id)

    if approved:
        approved.status = status
        approved.save()
        messages.success(request, success_message)
        return redirect('received_jobs')

    messages.error(request, 'Invalid request method.')
    return redirect('received_jobs')
