from django.contrib import admin
from .models import Project, Tag

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('tags')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
