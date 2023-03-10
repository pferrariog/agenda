from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.shortcuts import render
from .models import ContactForm
from pathlib import Path
from yaml import safe_load


def login(request):
    if request.method != 'POST':
        return render(request, Path('accounts/login.html'))

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Wrong username or password!')
        return render(request, Path('accounts/login.html'))

    auth.login(request, user)
    messages.success(request, 'Sucessfully logged in!')
    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    register_path = Path('accounts/register.html')
    if request.method != 'POST':
        return render(request, register_path)

    name = request.POST.get('name').title()
    last_name = request.POST.get('last_name').title()
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_valid = request.POST.get('password_valid')

    fields = [name, last_name, email, username, password, password_valid]

    if any(not field for field in fields):
        messages.error(request, 'Fields cannot be empty!')
        return render(request, register_path)

    if len(username) < 4:
        messages.error(request, 'Username too short!')
        return render(request, register_path)

    try:
        validate_email(email)
    except Exception:
        messages.error(request, 'Invalid email!')
        return render(request, register_path)

    with open(Path('users.yaml')) as user_file:
        allowed_users = safe_load(user_file)
        if email not in allowed_users['allowed_users']:
            messages.error(request, 'User creation with this e-mail is not allowed!')
            return render(request, register_path)

    if len(password) < 7:
        messages.error(request, 'Too short password!')
        return render(request, register_path)

    if password != password_valid:
        messages.error(request, "Passwords doesn't match!")
        return render(request, register_path)

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists!")
        return render(request, register_path)

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists!")
        return render(request, register_path)

    messages.success(request, 'Successfully registered user! Now you can login.')
    user = User.objects.create_user(
        username=username, email=email, password=password, first_name=name, last_name=last_name
    )
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = ContactForm()
        return render(request, Path('accounts/dashboard.html'), {'form': form})

    form = ContactForm(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'An error occurred while trying to send the form!')
        form = ContactForm(request.POST)
        return render(request, Path('accounts/dashboard.html'), {'form': form})

    form.save()
    messages.success(request, f'Contact {request.POST.get("name")} {request.POST.get("last_name")} created!')
    return redirect('dashboard')
