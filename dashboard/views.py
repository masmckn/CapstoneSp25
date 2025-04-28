from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from dashboard.models import Payment
import json
from decimal import Decimal 
from django.utils import timezone

# Dictionary to map expense types to insurance policy fields
insurance_mapping = {
            'specialist': ('specialistfee', 'specialistfeetype'),
            'other_physician': ('otherfee', 'otherfeetype'),
            'preventive': ('preventivefee', 'preventivefeetype'),
            'diagnostic': ('diagnosticfee', 'diagnosticfeetype'),
            'imaging': ('imagingfee', 'imagingfeetype'),
            'generic': ('genericfee', 'genericfeetype'),
            'preferred_brand': ('prefbrandfee', 'prefbrandfeetype'),
            'nonpreferred_brand': ('npbrandfee', 'npbrandfeetype'),
            'specialty': ('specialtyfee', 'specialtyfeetype'),
            'facility': ('facilityfee', 'facilityfeetype'),
            'primary': ('primaryfee', 'primaryfeetype'),
            'er': ('erfee', 'erfeetype'),
            'transport': ('transportfee', 'transportfeetype'),
            'urgent': ('ucfee', 'ucfeetype'),
            'mental_health_inpatient': ('mhinpatientfee', 'mhinpatientfeetype'),
            'mental_health_outpatient': ('mhoutpatientfee', 'mhoutpatientfeetype'),
            'substance_use_outpatient': ('suoutpatientfee', 'suoutpatientfeetype'),
            'substance_use_inpatient': ('suinpatientfee', 'suinpatientfeetype'),
            'prenatal': ('prenatalfee', 'prenatalfeetype'),
            'delivery': ('deliveryfee', 'deliveryfeetype'),
            'home_care': ('homecarefee', 'homecarefee'),
            'rehab': ('rehabfee', 'rehabfeetype'),
            'habilitation': ('habilitationfee', 'habilitationfeetype'),
            'skilled_nursing': ('skilledfee', 'skilledfeetype'),
            'equipment': ('equipmentfee', 'equipmentfeetype'),
            'hospice': ('hospicefee', 'hospicefeetype'),
        }

# Create your views here.
@login_required
def dashboard(request):
    insurance = request.user.insurancepolicy_set.get()
    expense_list = None
    total_due = 0
    past_payments = None
    last_payment = None

    if request.user.expense_set.exists():
        expense_list = request.user.expense_set.all()

        for expense in expense_list:
            if not expense.payment_id:
                # Get the corresponding insurance fields for this expense type
                fee_field, type_field = insurance_mapping.get(expense.caretype, (None, None))
                
                if fee_field and type_field:
                    coverage_amount = getattr(insurance, fee_field, 0)
                    coverage_type = getattr(insurance, type_field, 'copay')
                    
                    if coverage_type == 'copay':
                        # For copay, subtract the fixed amount
                        out_of_pocket = max(0, coverage_amount)
                    else:  # coinsurance
                        # For coinsurance, calculate percentage (coverage_amount is the percentage)
                        out_of_pocket = expense.amtdue * (Decimal(coverage_amount) / Decimal('100'))
                    
                    total_due += out_of_pocket

    if request.user.payment_set.exists():
        past_payments = request.user.payment_set.order_by('-day_paid')
        # Get the last payment if there are any payments
        last_payment = past_payments.first()
    context = {'username': request.user.username, 'email': request.user.email, 'first_name': request.user.first_name,
               'phonenum': request.user.userprofile.phone_number, 'provider': insurance.provider,
               'policy': insurance.policynum, 'deductible': insurance.generaldeductible, 'past_payments': past_payments,
               'expense_list': expense_list, 'total_due': total_due, 'last_payment': last_payment}
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def user_profile(request):
    fullname = request.user.first_name + " " + request.user.last_name
    insurance = request.user.insurancepolicy_set.get()
    context = {'full_name': fullname, 'phonenum': request.user.userprofile.phone_number,
               'policy': insurance.policynum, 'provider': insurance.provider} 
    return render(request, 'dashboard/profile.html', context)

@login_required
def change_pass(request):
    if(request.method == "POST"):
        # Get form data
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Match passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/profile/')

        # Update the user's password
        request.user.set_password(password)
        request.user.save()  # Save the User object first

        update_session_auth_hash(request, request.user)
        
        messages.success(request, "Password updated successfully!")
    return redirect('/profile/')

@login_required
def payment(request):
    if request.method == 'POST':
        insurance = request.user.insurancepolicy_set.get()
        amount = int(request.POST.get('amount'))
        remaining_amount = amount
        
        # Create the payment record
        payment = Payment.objects.create(
            amount=amount,
            day_paid=timezone.now().date(),  # Using .date() since it's a DATE field
            username=request.user
        )
        
        # Get unpaid expenses ordered by due date
        unpaid_expenses = request.user.expense_set.filter(
            payment_id=None  # Unpaid expenses have no payment_id
        ).order_by('duedate')

        # Iterate through expenses and mark as paid
        for expense in unpaid_expenses:
            oopcost = 0
            fee_field, type_field = insurance_mapping.get(expense.caretype, (None, None))
            
            if fee_field and type_field:
                coverage_amount = getattr(insurance, fee_field, 0)
                coverage_type = getattr(insurance, type_field, 'copay')
                
                if coverage_type == 'copay':
                    # For copay, subtract the fixed amount
                    out_of_pocket = max(0, coverage_amount)
                else:  # coinsurance
                    # For coinsurance, calculate percentage (coverage_amount is the percentage)
                    out_of_pocket = expense.amtdue * (coverage_amount / 100.0)
                
                oopcost += out_of_pocket

            if remaining_amount >= oopcost:
                expense.payment_id = payment
                expense.save()
                payment.receiver = expense.debtsource
                payment.save()
                remaining_amount -= oopcost
            
            if remaining_amount <= 0:
                break

        return redirect('/dashboard/')
    context = {}
    return render(request, 'dashboard/payment.html', context)

@login_required
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('/login/')


@login_required
def insurance_details(request):
    insurance = request.user.insurancepolicy_set.get()

    fee_mapping = {
        "specialist_fee": "specialistfee",
        "other_physician_fee": "otherfee",
        "preventive_care_fee": "preventivefee",
        "diagnostic_care_fee": "diagnosticfee",
        "imaging_fee": "imagingfee",
        "generic_prescription_fee": "genericfee",
        "preferred_brand_prescription_fee": "prefbrandfee",
        "nonpreferred_brand_prescription_fee": "npbrandfee",
        "specialty_fee": "specialtyfee",
        "facility_care_fee": "facilityfee",
        "primary_fee": "primaryfee",
        "er_fee": "erfee",
        "transport_fee": "transportfee",
        "urgent_care_fee": "ucfee",
        "mental_healthcare_inpatient_fee": "mhinpatientfee",
        "mental_healthcare_outpatient_fee": "mhoutpatientfee",
        "substance_use_outpatient_fee": "suoutpatientfee",
        "substance_use_inpatient_fee": "suinpatientfee",
        "prenatal_care_fee": "prenatalfee",
        "birth_delivery_fee": "deliveryfee",
        "home_care_fee": "homecarefee",
        "rehabilitation_facility_fee": "rehabfee",
        "habilitation_fee": "habilitationfee",
        "skilled_nursing_fee": "skilledfee",
        "equipment_fee": "equipmentfee",
        "hospice_care_fee": "hospicefee",
    }

    if request.method == 'POST':
        print(request.POST)
        for form_field, db_column in fee_mapping.items():
            value = request.POST.get(form_field)
            print('Looking for {}'.format(form_field))
            if value:
                setattr(insurance, db_column, value)

            type_field = f"{form_field}_type"
            print('Looking for {}'.format(type_field))
            type_value = request.POST.get(type_field)
            if type_value: 
                type_column = f"{db_column}type"
                setattr(insurance, type_column, type_value)
        insurance.save()
    fee_values = {
        fee: {
            'value': float(getattr(insurance, db_column, 0)) if isinstance(getattr(insurance, db_column, None), Decimal) else getattr(insurance, db_column, None),
            'type': getattr(insurance, f"{db_column}type", 'copay')
        }
        for fee, db_column in fee_mapping.items()
    }

    context = {'fee_values_json': json.dumps(fee_values), 'primaryfee': insurance.primaryfee}
    return render(request, 'dashboard/insurancedetails.html', context)