from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Contact
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib import messages
from pathlib import Path


def index(request):
    contacts = Contact.objects.order_by('name').filter(
        show=True
    )
    paginator = Paginator(contacts, 3)

    page = request.GET.get('page')
    contacts_per_page = paginator.get_page(page)
    return render(request, Path('contacts/index.html'), {
        "contacts": contacts_per_page
    })


def profile(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.show:
        raise Http404
    return render(request, Path('contacts/profile.html'), {
        "contact": contact
    })


def search(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        messages.add_message(request, messages.ERROR, 'Search field cannot be empty!')
        return redirect('index')
    title_keyword = keyword.title()
    fields = Concat('name', Value(' '), 'last_name')  # value simulate a field in db
    contacts = Contact.objects.annotate(
        full_name=fields
    ).filter(
        Q(full_name__icontains=title_keyword) | Q(phone__icontains=title_keyword)
    )
    paginator = Paginator(contacts, 3)
    page = request.GET.get('page')
    contacts_per_page = paginator.get_page(page)
    return render(request, Path('contacts/index.html'), {
        "contacts": contacts_per_page
    })

