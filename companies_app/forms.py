from django.forms import CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView

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
    class Meta:
        model = Company
        fields = ['title', 'phone']


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['title', 'size', 'category']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_name', 'city', 'state', 'house_number']