from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.shortcuts import render


def login(request):
    return render(request, r'accounts\login.html')


def logout(request):
    return render(request, r'accounts\logout.html')


def register(request):
    if request.method != 'POST':
        return render(request, r'accounts\register.html')

    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_valid = request.POST.get('password_valid')

    fields = [name, last_name, email, username, password, password_valid]

    if any(not field for field in fields):
        messages.error(request, 'Fields cannot be empty!')
        return render(request, r'accounts\register.html')

    if len(username) < 4:
        messages.error(request, 'Username too short!')
        return render(request, r'accounts\register.html')

    try:
        validate_email(email)
    except Exception:
        messages.error(request, 'Invalid email!')
        return render(request, r'accounts\register.html')

    if len(password) < 7:
        messages.error(request, 'Too short password!')
        return render(request, r'accounts\register.html')

    if password != password_valid:
        messages.error(request, "Passwords doesn't match!")
        return render(request, r'accounts\register.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists!")
        return render(request, r'accounts\register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists!")
        return render(request, r'accounts\register.html')

    messages.success(request, 'Successfully registered user! Now you can login.')
    user = User.objects.create_user(
        username=username, email=email, password=password, first_name=name, last_name=last_name
    )
    user.save()
    return redirect('login')


def dashboard(request):
    return render(request, r'accounts\dashboard.html')
