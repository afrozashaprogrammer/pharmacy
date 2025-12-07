from django.db import models

# Create your models here.
class MedicalTest(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(
        max_length=10,
        choices=[
            ('percent', 'Percentage'),
            ('flat', 'Flat Amount'),
        ],
        blank=True,
        null=True
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Sample
    sample_type = models.CharField(
        max_length=100,
        choices=[
            ('blood', 'Blood'),
            ('urine', 'Urine'),
            ('stool', 'Stool'),
            ('saliva', 'Saliva'),
            ('xray', 'Xray'),
            ('ct', 'CT Scan'),
            ('mri', 'MRI'),
            ('ultrasound', 'Ultrasound'),
        ],
        blank=True, null=True
    )
    fasting_required = models.BooleanField(default=False)
    processing_time_hours = models.PositiveIntegerField(default=24)

    # Report Related
    unit = models.CharField(max_length=50, blank=True, null=True)
    has_range = models.CharField(max_length=255, blank=True, null=True)
    report_format = models.CharField(
        max_length=50,
        choices=[
            ('pdf', 'PDF'),
            ('text', 'Text'),
            ('image', 'Image'),
        ],
        default='pdf'
    )
    reference_range = models.CharField(max_length=200, blank=True, null=True)
    # Demographics
    gender_specific = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Both', 'Both')],
        default='Both'
    )
    # Extra
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
