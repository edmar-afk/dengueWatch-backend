from django.contrib import admin
from .models import DengueLocation, Residents


admin.site.register(Residents)
admin.site.register(DengueLocation)