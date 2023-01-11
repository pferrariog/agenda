from django.shortcuts import render


def index(request):
    return render(request, r'contacts\index.html')
