# notes/forms.py

"""
This module defines forms used within the Note application. The forms
in this module extend Django's inbuilt 'forms.ModelForm' module to use
Django's functionality for creating and processing forms.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating Note objects.

    Fields
    ------
    title (TextInput):
        CharField for the note's title. This field uses bootstrap
        classes to improve its appearance.
    content (Textarea):
        Textarea for the note's content, also styled with bootstrap
        classes.

    Meta class
    ----------
    Defines the model to use (Note) and the fields to include in the
    form.

    :param forms.ModelForm: Django's ModelForm class.
    """

    class Meta:
        """
        Defines the model to use (Note) and the fields to include in the
        form.

        Attributes
        ----------
        model (Model):
            The model class representing the database table this form
            interacts with.
        fields (list):
            A list of strings that specifies which model fields should
            be included in the form.
        widgets (dict):
            Configuration of widgets used for rendering fields. Each
            widget is mapped to a model field to define how the field
            appears in the HTML form output.

        :param forms.ModelForm: Django's ModelForm class.
        """

        # Define model and the fields for the form
        model = Note
        fields = ["title", "content"]

        # Create widget attrs to use with Bootstrap
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control form-title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control form-content",
                }
            ),
        }


class SignUpForm(UserCreationForm):
    """
    A form for registering new users. Extends Django's UserCreationForm
    to include an email field in addition to the username and password
    fields provided by default.

    Attributes
    -----------
    email (forms.EmailField):
        An additional email field with validations for input format
        and maximum length.

    Fields
    ------
    username (TextInput):
        TextInput for the username. This field uses bootstrap
        classes to improve its appearance.
    email (EmailInput):
        EmailInput for the user's email address which is also
        styled with bootstrap classes.
    password1 (PasswordInput):
        PasswordInput for the user's password, also styled with
        bootstrap classes.
    password2 (PasswordInput):
        PasswordInput for a confirmation of the user's password,
        also styled with bootstrap classes.

    Meta class
    ----------
    Subclass for specifying model behaviour options in the SignUpForm.

    :param forms.ModelForm: Django's ModelForm class.
    """

    # Define email field
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.'
    )

    class Meta:
        """
        Meta subclass for specifying model behaviour options in the
        SignUpForm.

        Overrides the model field from UserCreationForm.Meta to include
        the email field in addition to username, password1, and
        password2 required during user registration.

        Attributes
        ----------
        model (Model):
            The user model associated with the form.
        fields (list):
            Specifies the order of fields in the form, which impacts
            their render order on the frontend.
        widgets (dict):
            Configuration of widgets used for rendering fields. Each
            widget is mapped to a model field to define how the field
            appears in the HTML form output.

        :param forms.ModelForm: Django's ModelForm class.
        """

        # Define model and the fields for the form
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        # Create widget attrs to use with Bootstrap
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
