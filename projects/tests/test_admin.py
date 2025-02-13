import unittest
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from projects.models import Project, Tag
from projects.admin import ProjectAdmin, TagAdmin

User = get_user_model()


class DummyRequest:
    def __init__(self, user):
        self.user = user


class TestAdmin(TestCase):
    def setUp(self):
        # Create an admin user for authentication
        self.admin_user = User.objects.create_superuser(
            username='admintest',
            email='admin@example.com',
            password='admin-password'
        )
        self.factory = RequestFactory()
        self.site = AdminSite()

        # Create initial objects
        self.project = Project.objects.create(
            title='Example Project',
            description='This is an example project',
                                              )
        self.tag = Tag.objects.create(name='Example Tag')
        self.client.force_login(self.admin_user)

    def test_project_admin_list_display(self):
        # Instantiate the admin class for Project
        project_admin = ProjectAdmin(Project, self.site)
        request = DummyRequest(self.admin_user)
        list_display = project_admin.get_list_display(request)
        self.assertIn('title', list_display)
        # You can add asserts for other fields or custom methods

    def test_tag_admin_search_fields(self):
        tag_admin = TagAdmin(Tag, self.site)
        request = DummyRequest(self.admin_user)
        search_fields = tag_admin.get_search_fields(request)
        self.assertTrue(len(search_fields) > 0)
        # Ensure expected search fields are included

    def test_admin_add_view_permissions(self):
        # Using Django's test client to ensure the add view works
        self.client.force_login(self.admin_user)
        response = self.client.get('/admin/projects/project/add/')
        self.assertEqual(response.status_code, 200)
        # Similarly, test the change view.

    def test_admin_can_access_project_list(self):
        response = self.client.get('/admin/projects/project/')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_edit_project(self):
        url = reverse('admin:projects_project_change', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

