from django.contrib import admin
from django import forms
from .models import Project, Tag

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'live_url', 'github_url')
    search_fields = ('title', 'description')
    list_filter = ('tags',) #Must be tuple

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'live_url', 'github_url', 'tags']

    def clean_live_url(self):
        url = self.cleaned_data['live_url']
        if not url.startswith('http'):
            url = 'http://' + url
        return url

