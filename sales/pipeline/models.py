from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from PIL import Image

# Create your models here.
business_class_choices = (
    ('', 'Select'),
    ('MOTOR', 'MOTOR PRIVATE'),
    ('MOTOR', 'MOTOR COMMERCIAL'),
    ('ENGINEERING', 'ENGINEERING'),
    ('FIRE', 'FIRE DOMESTIC'),
    ('FIRE', 'FIRE INDUSTRIAL'),
    ('LIABILITIES', 'LIABILITIES'),
    ('MARINE', 'MARINE'),
    ('PA', 'PERSONAL ACCIDENT'),
    ('THEFT', 'THEFT'),
    ('WIBA', 'WORKMEN\'S COMPENSATION'),
    ('MISCELLANEOUS', 'MISCELLANEOUS'),
    ('MEDICAL', 'MEDICAL'),
)

chances_of_closure_choices = (
    ('', 'Select'),
    ('LOW', 'LOW'),
    ('MEDIUM', 'MEDIUM'),
    ('HIGH', 'HIGH'),
    ('CLOSED', 'CLOSED'),
)

current_stage_choices = (
    ('', 'Select'),
    ('Prospecting', 'Prospecting'),
    ('Introduction', 'Introduction'),
    ('Quotation', 'Quotation'),
    ('Negotiation', 'Negotiation'),
    ('KYC', 'KYC Collection'),
    ('Payment', 'Payment'),
    ('Debiting', 'Debiting'),
    ('Closed', 'Closed'),
    ('Lost', 'Lost'),
)

class Record(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first, null=False, related_name='created_records')
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    nearest_town = models.CharField(max_length=200, null=True, blank=True)
    current_insurer = models.CharField(max_length=125, null=True, blank=True)
    intermediary_name = models.CharField(max_length=200, null=True, blank=True)
    engagement_date = models.DateField(null=True, blank=True)
    updated_date = models.DateField(auto_now=True)
    anticipated_closure_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    business_class = models.CharField(max_length=15, null=True, blank=True, choices=business_class_choices,)
    expected_premium = models.IntegerField(default=0)
    chances_of_closure = models.CharField(max_length=15, null=True, blank=True, choices=chances_of_closure_choices,)
    current_stage = models.CharField(max_length=15, null=True, blank=True, choices=current_stage_choices,)
    additional_remarks = models.TextField(null=True, blank=True)
    # created_by_ignore = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='record_created_by')

    def __str__(self):

        return self.first_name + "   " + self.last_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)   

# Automatically create a UserProfile instance for each new User
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, profile_pic='default.jpg')

# Connect the create_user_profile function to the User's post_save signal
models.signals.post_save.connect(create_user_profile, sender=User)