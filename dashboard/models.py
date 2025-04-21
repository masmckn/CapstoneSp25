from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class InsurancePolicy(models.Model):
    policynum = models.CharField(db_column='PolicyNum', primary_key=True, max_length=255, db_collation='utf8mb3_general_ci')  # Field name made lowercase.
    provider = models.CharField(db_column='Provider', max_length=255, db_collation='utf8mb3_general_ci')  # Field name made lowercase.
    generaldeductible = models.IntegerField(db_column='GeneralDeductible', blank=True, null=True)  # Field name made lowercase.
    ooplimit = models.IntegerField(db_column='OOPLimit', blank=True, null=True)  # Field name made lowercase.
    primaryfee = models.DecimalField(db_column='PrimaryFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    primaryfeetype = models.CharField(db_column='PrimaryFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    specialistfee = models.DecimalField(db_column='SpecialistFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    specialistfeetype = models.CharField(db_column='SpecialistFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    otherfee = models.DecimalField(db_column='OtherFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    otherfeetype = models.CharField(db_column='OtherFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    preventivefee = models.DecimalField(db_column='PreventiveFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    preventivefeetype = models.CharField(db_column='PreventiveFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    diagnosticfee = models.DecimalField(db_column='DiagnosticFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    diagnosticfeetype = models.CharField(db_column='DiagnosticFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    imagingfee = models.DecimalField(db_column='ImagingFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    imagingfeetype = models.CharField(db_column='ImagingFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    genericfee = models.DecimalField(db_column='GenericFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    genericfeetype = models.CharField(db_column='GenericFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    prefbrandfee = models.DecimalField(db_column='PrefBrandFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    prefbrandfeetype = models.CharField(db_column='PrefBrandFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    npbrandfee = models.DecimalField(db_column='NPBrandFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    npbrandfeetype = models.CharField(db_column='NPBrandFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    specialtyfee = models.DecimalField(db_column='SpecialtyFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    specialtyfeetype = models.CharField(db_column='SpecialtyFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    facilityfee = models.DecimalField(db_column='FacilityFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    facilityfeetype = models.CharField(db_column='FacilityFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    physicianfee = models.DecimalField(db_column='PhysicianFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    physicianfeetype = models.CharField(db_column='PhysicianFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    erfee = models.DecimalField(db_column='ERFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    erfeetype = models.CharField(db_column='ERFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    transportfee = models.DecimalField(db_column='TransportFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transportfeetype = models.CharField(db_column='TransportFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ucfee = models.DecimalField(db_column='UCFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ucfeetype = models.CharField(db_column='UCFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    mhoutpatientfee = models.DecimalField(db_column='MHOutpatientFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mhoutpatientfeetype = models.CharField(db_column='MHOutpatientFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    mhinpatientfee = models.DecimalField(db_column='MHInpatientFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mhinpatientfeetype = models.CharField(db_column='MHInpatientFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    suoutpatientfee = models.DecimalField(db_column='SUOutpatientFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    suoutpatientfeetype = models.CharField(db_column='SUOutpatientFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    suinpatientfee = models.DecimalField(db_column='SUInpatientFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    suinpatientfeetype = models.CharField(db_column='SUInpatientFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    prenatalfee = models.DecimalField(db_column='PrenatalFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    prenatalfeetype = models.CharField(db_column='PrenatalFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    deliveryfee = models.DecimalField(db_column='DeliveryFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    deliveryfeetype = models.CharField(db_column='DeliveryFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    homecarefee = models.DecimalField(db_column='HomeCareFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    homecarefeetype = models.CharField(db_column='HomeCareFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    rehabfee = models.DecimalField(db_column='RehabFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rehabfeetype = models.CharField(db_column='RehabFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    habilitationfee = models.DecimalField(db_column='HabilitationFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    habilitationfeetype = models.CharField(db_column='HabilitationFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    skilledfee = models.DecimalField(db_column='SkilledFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    skilledfeetype = models.CharField(db_column='SkilledFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    equipmentfee = models.DecimalField(db_column='EquipmentFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    equipmentfeetype = models.CharField(db_column='EquipmentFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    hospicefee = models.DecimalField(db_column='HospiceFee', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    hospicefeetype = models.CharField(db_column='HospiceFeeType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    username = models.ForeignKey(User, models.CASCADE, db_column='username', to_field='username', blank=True, null=True)

    class Meta:
        db_table = 'insurancepolicy'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'userprofile'

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    id = models.AutoField(primary_key=True) # Auto-incrementing primary key
    amount = models.IntegerField() # Amount field
    day_paid = models.DateField() # Date field for when the payment was made
    day_processed = models.DateField(null=True, blank=True) # Date field for when the payment was processed
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', db_column='username', null=True, blank=True)

    class Meta:
        db_table = 'payment'