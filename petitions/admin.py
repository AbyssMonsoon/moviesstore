from django.contrib import admin
from .models import Petition

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'yes_count')
    search_fields = ('title', 'description', 'created_by__username')
