from django import forms
from .models import PackageCategory

class PackageCategoryForm(forms.ModelForm):
    class Meta:
        model = PackageCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'categoryName',
                'name': 'categoryName'
            })
        }
        labels = {
            'name': 'Category Name'
        }
