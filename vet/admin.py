from django.contrib import admin
from .models import VetProfile, VetService, VetBooking

admin.site.register(VetProfile)
admin.site.register(VetService)
admin.site.register(VetBooking)
