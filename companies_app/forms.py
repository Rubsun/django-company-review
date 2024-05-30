from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField

from companies_app.models import Review, Company, Equipment, Address


class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']


class CompanyForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Company
        fields = ['title', 'phone']


class EquipmentForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Equipment
        fields = ['title', 'size', 'category']


class AddressForm(forms.ModelForm):
    street_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Address
        fields = ['street_name', 'city', 'state', 'house_number']
