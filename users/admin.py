from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display=('bio', 'liked')
    list_filter=('bio', 'liked')
