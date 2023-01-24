from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.shortcuts import render


def login(request):
    if request.method != 'POST':
        return render(request, r'accounts\login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Wrong username or password!')
        return render(request, r'accounts\login.html')

    auth.login(request, user)
    messages.success(request, 'Sucessfully logged in!')
    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, r'accounts\register.html')

    name = request.POST.get('name').title()
    last_name = request.POST.get('last_name').title()
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


@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, r'accounts\dashboard.html')
