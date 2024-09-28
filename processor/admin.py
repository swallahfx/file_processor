from django.contrib import admin

from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['source_file', 'target_file', 'uploaded_at']
    readonly_fields = ['uploaded_at']
