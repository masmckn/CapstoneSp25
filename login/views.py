from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from dashboard.models import InsurancePolicy, UserProfile
from django.contrib import messages


def log_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, "login/login.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect('/login/')

def create_account(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        insurance = request.POST.get('insurance')
        policy_number = request.POST.get('policy_number')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'login/createaccount.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'login/createaccount.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'login/createaccount.html')

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        UserProfile.objects.create(
            user=user,
            phone_number=phone,
            address=address
        )

        InsurancePolicy.objects.create(
            policynum=policy_number,
            provider=insurance,
            username=user
        )

        messages.success(request, "Account created successfully!")
        return redirect('log_user')

    return render(request, 'login/createaccount.html')
