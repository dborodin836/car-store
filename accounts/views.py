from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.ERROR(request, "Username already exists")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.ERROR(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name,
                                                    last_name=last_name,
                                                    username=username,
                                                    email=email,
                                                    password=password)
                    user.save()
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in.')
                    return redirect('dashboard')
        else:
            messages.error(request, "Password do not match.")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard(request):
    user_inqiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)

    data = {
        'inquires': user_inqiry
    }
    return render(request, 'accounts/dashboard.html', data)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
