from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Residents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dengue_status = models.TextField(default='No Dengue History')
    phone_number = models.CharField(max_length=15)
    location = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    resident_idCard = models.ImageField(upload_to='resident_idcards/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    def __str__(self):
        return self.full_name
    
    
class DengueLocation(models.Model):
    status = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="dengue_reports/", blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.TextField(blank=True, null=True)
               
    def __str__(self):
        return self.description
    

from django.db import models

class DengueCase(models.Model):
    resident = models.ForeignKey(Residents,on_delete=models.CASCADE, related_name="dengue_cases")
    status = models.TextField(blank=True, null=True)
    date_case = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resident.full_name} - {self.status}"