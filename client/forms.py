# forms.py (inside your photographer app)

from django import forms
from .models import HiringDetails

class HiringForm(forms.ModelForm):
    class Meta:
        model = HiringDetails
        fields = [ 'client_name','client_email', 'phone', 'address', 'starting_date', 'detail_message']
