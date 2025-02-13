from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from projects.models import Project, Tag


class TestProjectAPIs(APITestCase):
    def setUp(self):
        # Create tags
        self.tag_python = Tag.objects.create(name='Python')
        self.tag_django = Tag.objects.create(name='Django')

        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description'
        )
        self.project.tags.add(self.tag_python)

        # Create test project
        self.valid_project_data = {
            'title': 'New Project',
            'description': 'Project description',
            'github_url': 'https://github.com/example',
            'live_url': 'https://example.com',
            'tags': [self.tag_python.id, self.tag_django.id],
        }

        # Project data for creation tests
        self.valid_project_data = {
            'title': 'New Project',
            'description': 'New project description',
            'github_url': 'https://github.com/test/new',
            'live_url': 'https://new.com',
            'tags': [self.tag_python.id, self.tag_django.id]
        }

        self.invalid_project_data = {
            'description': 'Missing title'
        }

    def test_list_projects_api(self):
        url = reverse('projects:api_project_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.project.title)

    def test_create_project_api(self):
        url = reverse('projects:api_project_list')
        response = self.client.post(url, self.valid_project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.get(title='New Project').tags.count(), 2)

    def test_create_invalid_project_api(self):
        url = reverse('projects:api_project_list')
        response = self.client.post(url, self.invalid_project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_detail_api(self):
        url = reverse('projects:api_project_detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project.title)
        self.assertEqual(response.data['description'], self.project.description)
        self.assertEqual(response.data['github_url'], self.project.github_url)
        self.assertEqual(response.data['live_url'], self.project.live_url)
        self.assertIn('tags', response.data)

    def test_project_detail_api_404(self):
        url = reverse('projects:api_project_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project_api(self):
        url = reverse('projects:api_project_detail', args=[self.project.id])
        update_data = {
            'title': 'Updated Project',
            'description': 'Updated description',
            'tags': [self.tag_django.id]
        }
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project')
        self.assertEqual(self.project.tags.first(), self.tag_django)

    def test_delete_project_api(self):
        url = reverse('projects:api_project_detail', args=[self.project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_create_project_without_optional_fields(self):
        url = reverse('projects:api_project_list')
        minimal_data = {
            'title': 'Minimal Project',
            'description': 'Only required fields'
        }
        response = self.client.post(url, minimal_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['github_url'])
        self.assertIsNone(response.data['live_url'])

    def test_list_projects_empty(self):
        Project.objects.all().delete()
        url = reverse('projects:api_project_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_partial_update_project_api(self):
        url = reverse('projects:api_project_detail', args=[self.project.id])
        partial_update = {'title': 'Partially Updated'}
        response = self.client.patch(url, partial_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Partially Updated')
        self.assertEqual(self.project.description, 'Test Description')
