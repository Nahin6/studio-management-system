from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['photographerName','packageName','type', 'img', 'cover_img', 'duration', 'description', 'price']

    def clean_photographerName(self):
        photographerName = self.cleaned_data.get('photographerName')
        if not photographerName:
            raise forms.ValidationError("Photographer name cannot be empty.")
        return photographerName
    def clean_packageName(self):
        packageName = self.cleaned_data.get('packageName')
        if not packageName:
            raise forms.ValidationError("package name cannot be empty.")
        return packageName

    def clean_img(self):
        img = self.cleaned_data.get('img')
        if not img:
            raise forms.ValidationError("Please upload an image.")
        return img

    def clean_cover_img(self):
        cover_img = self.cleaned_data.get('cover_img')
        if not cover_img:
            raise forms.ValidationError("Please upload a cover image.")
        return cover_img

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            raise forms.ValidationError("Duration cannot be empty.")
        return duration

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Description cannot be empty.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price:
            raise forms.ValidationError("Price cannot be empty.")
        return price
