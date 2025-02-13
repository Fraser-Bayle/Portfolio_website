from django.db import models
from rest_framework.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Project Tag"
        verbose_name_plural = "Project Tags"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    # Example ManyToMany relation for tags
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)


    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at', 'title']

    thumbnail = models.ImageField(upload_to='project_thumbnails/', blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.title:
            raise ValidationError('Project title is required')
        if not self.description:
            raise ValidationError('Project description is required')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('project:detail', args=[self.id])
