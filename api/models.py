from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Residents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dengue_status = models.TextField(default='Safe')
    phone_number = models.CharField(max_length=15)
    location = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.full_name
    
    
class DengueLocation(models.Model):
    status = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description