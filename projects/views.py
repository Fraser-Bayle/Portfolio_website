from django.shortcuts import render, get_object_or_404
from .models import Project, Tag

def project_list(request):
    tag_name = request.GET.get('tag', None)
    if tag_name:
        projects = Project.objects.filter(tags__name__iexact=tag_name).order_by('-created_at')
    else:
        projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
