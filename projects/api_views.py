from rest_framework import generics
from .models import Project
from .serializer import ProjectSerializer


class ProjectsListAPI(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        # Get tags from the request data
        tags = self.request.data.get('tags', [])
        # Save the project first
        project = serializer.save()
        # Set the tags
        project.tags.set(tags)


class ProjectsDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def perform_update(self, serializer):
        # Get tags from the request data
        tags = self.request.data.get('tags', None)
        # Keep existing data for partial updates
        instance = self.get_object()
        # Save with partial=True for PATCH requests
        project = serializer.save(
            description=self.request.data.get('description', instance.description),
        )
        # Only update tags if they were provided in the request
        if tags is not None:
            project.tags.set(tags)
