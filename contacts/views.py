from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Contact


def index(request):
    contacts = Contact.objects.all()
    return render(request, r'contacts\index.html', {
        "contacts": contacts
    })


def profile(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, r'contacts\profile.html', {
        "contact": contact
    })
