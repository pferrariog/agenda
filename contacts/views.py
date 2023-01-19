from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Contact


def index(request):
    contacts = Contact.objects.order_by('name').filter(
        show=True
    )
    paginator = Paginator(contacts, 1)

    page = request.GET.get('page')
    contacts_per_page = paginator.get_page(page)
    return render(request, r'contacts\index.html', {
        "contacts": contacts_per_page
    })


def profile(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.show:
        raise Http404
    return render(request, r'contacts\profile.html', {
        "contact": contact
    })
