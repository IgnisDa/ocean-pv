from django.contrib import admin
from .models import UserProfile, ProfileRelation

admin.site.register(UserProfile)
admin.site.register(ProfileRelation)
