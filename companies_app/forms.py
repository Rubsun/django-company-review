"""
This module defines various forms used in the `companies_app` application.

The forms are used for user registration, login, and managing instances of
models such as Review, Company, Equipment, and Address.

Classes:
    - RegistrationForm: A form for user registration.
    - LoginForm: A form for user login.
    - ReviewForm: A form for creating and editing reviews.
    - CompanyForm: A form for creating and editing companies.
    - EquipmentForm: A form for creating and editing equipment.
    - AddressForm: A form for creating and editing addresses.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField

from companies_app.models import Address, Company, Equipment, Review

FORM_CONTROL = 'form-control'
CLASS = 'class'


class RegistrationForm(UserCreationForm):
    """
    A form for user registration that extends the built-in UserCreationForm.

    Fields:
    - username: The desired username for the new user.
    - first_name: The first name of the new user.
    - last_name: The last name of the new user.
    - email: The email address of the new user.
    - password1: The password for the new user.
    - password2: The password confirmation for the new user.
    """

    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = CharField(max_length=100, required=True)

    class Meta:
        """Meta."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    """
    A form for user login.

    Fields:
    - username: The username of the user.
    - password: The password of the user.
    """

    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class ReviewForm(forms.ModelForm):
    """
    A form for creating and editing reviews.

    Fields:
    - text: The text content of the review.
    - rating: The rating given in the review.
    """

    class Meta:
        """Meta."""

        model = Review
        fields = ['text', 'rating']


class CompanyForm(forms.ModelForm):
    """
    A form for creating and editing companies.

    Fields:
    - title: The title of the company.
    - phone: The phone number of the company.
    """

    title = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={CLASS: FORM_CONTROL}),
    )
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={CLASS: FORM_CONTROL}))

    class Meta:
        """Meta."""

        model = Company
        fields = ['title', 'phone']


class EquipmentForm(forms.ModelForm):
    """
    A form for creating and editing equipment.

    Fields:
    - title: The title of the equipment.
    - size: The size of the equipment.
    - category: The category to which the equipment belongs.
    """

    title = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={CLASS: FORM_CONTROL}),
    )

    class Meta:
        """Meta."""

        model = Equipment
        fields = ['title', 'size', 'category']


class AddressForm(forms.ModelForm):
    """
    A form for creating and editing addresses.

    Fields:
    - street_name: The street name of the address.
    - city: The city of the address.
    - state: The state of the address.
    - house_number: The house number of the address.
    """

    street_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={CLASS: FORM_CONTROL}),
    )
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={CLASS: FORM_CONTROL}))
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={CLASS: FORM_CONTROL}))

    class Meta:
        """Meta."""

        model = Address
        fields = ['street_name', 'city', 'state', 'house_number']
