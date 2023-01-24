from contacts.models import Contact
from django import forms
from django.db import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('show', 'creation_date')
