from django.contrib import admin
from .models import FilesAdmin

class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','downloadcount', 'emailcount',)
    list_filter =  ('downloadcount', 'emailcount')
    search_fields = ('title', 'description')

admin.site.register(FilesAdmin, FileAdmin)