from django.shortcuts import render, get_object_or_404
from .models import Project, Tag

def project_list(request):
    selected_tag_ids = request.GET.getlist('tags')
    projects = Project.objects.all()
    active_tags = []

    if selected_tag_ids:
        projects = projects.filter(tags__id__in=selected_tag_ids).distinct()
        active_tags = Tag.objects.filter(id__in=selected_tag_ids)

    context = {
        'projects': projects,
        'all_tags': Tag.objects.all(),
        'active_tags': active_tags,
    }

    return render(request, 'projects/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
