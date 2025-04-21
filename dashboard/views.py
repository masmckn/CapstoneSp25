from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import InsurancePolicy, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


# Create your views here.
@login_required
def dashboard(request):
    insurance = request.user.insurancepolicy_set.get()
    context = {'username': request.user.username, 'email': request.user.email, 'first_name': request.user.first_name,
               'phonenum': request.user.userprofile.phone_number, 'provider': insurance.provider,
               'policy': insurance.policynum, 'deductible': insurance.generaldeductible}
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def user_profile(request):
    fullname = request.user.first_name + " " + request.user.last_name
    insurance = request.user.insurancepolicy_set.get()
    context = {'full_name': fullname, 'phonenum': request.user.userprofile.phone_number,
               'address': request.user.userprofile.address, 'policy': insurance.policynum,
               'provider': insurance.provider} 
    return render(request, 'dashboard/profile.html', context)

@login_required
def update_account(request):
    if(request.method == "POST"):
        # Get form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        insurance = request.POST.get('insurance')
        policy_number = request.POST.get('policy_number')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Parse first name, last name from full name
        try:
            first, *middle, last = name.split()
        except ValueError:
            messages.error(request, "Please enter a valid first and last name.")
            return render(request, 'dashboard/profile.html')

        # Match passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'dashboard/profile.html')

        # Check if username already exists
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'dashboard/profile.html')

        # Check if email already exists
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'dashboard/profile.html')

        # Update the user object
        request.user.first_name = first
        request.user.last_name = last
        request.user.email = email
        request.user.username = username
        request.user.set_password(password)
        request.user.save()  # Save the User object first

        # Update UserProfile
        user_profile = request.user.userprofile  # Access the related UserProfile object
        user_profile.phone_number = phone
        user_profile.address = address
        user_profile.save()  # Save changes to UserProfile

        # Update InsurancePolicy
        try:
            insurance_policy = request.user.insurancepolicy_set.get()  # Retrieve the related InsurancePolicy
            insurance_policy.provider = insurance
            insurance_policy.policynum = policy_number
            insurance_policy.save()  # Save changes to InsurancePolicy
        except InsurancePolicy.DoesNotExist:
            messages.error(request, "No associated insurance policy found.")
            return render(request, 'dashboard/profile.html')

        update_session_auth_hash(request, request.user)
        
        messages.success(request, "Account updated successfully!")
    return redirect('user_profile')

@login_required
def payment(request):
    context = {}
    return render(request, 'dashboard/payment.html', context)