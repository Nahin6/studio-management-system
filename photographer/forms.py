from django import forms
from .models import Package
from .models import Income
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['photographerName','packageName','type', 'img', 'cover_img', 'duration', 'description', 'price']



class DebitForm(forms.Form):
    credit = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control',
            'id': 'credit',
        })
    )
    debit = forms.DecimalField(
        max_digits=10,
  
        label='Your Expense',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'debit',
        })
    )