from django.db import models
from django.contrib.auth.models import User
from administration.models import *

class PatientTest(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_tests"
    )

    referred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referred_patient_tests"
    )

    is_draft = models.BooleanField(default=True)
    sms_sent = models.BooleanField(default=False)

    total_item = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_average = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_paid = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="patienttest_created"
    )

    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="patienttest_updated"
    )

    def __str__(self):
        return f"PatientTest #{self.id}"

class PatientTestItem(models.Model):
    patient_test = models.ForeignKey(
        PatientTest,
        on_delete=models.CASCADE,
        related_name="items"
    )

    medical_test = models.ForeignKey(
        MedicalTest,
        on_delete=models.PROTECT
    )

    # snapshot fields (price/name change হলেও invoice stable থাকবে)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name



