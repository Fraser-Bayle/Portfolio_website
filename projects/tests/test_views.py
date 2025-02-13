from django.test import TestCase, Client
from django.urls import reverse
from projects.models import Project, Tag


class TestProjectViews(TestCase):
    def setUp(self):
        self.client = Client()
        # Use get_or_create to prevent duplicate tags
        self.tag_python, _ = Tag.objects.get_or_create(name='Python')
        self.tag_django, _ = Tag.objects.get_or_create(name='Django')

        # Create projects with different tag combinations
        self.project1 = Project.objects.create(
            title='Test Project 1',
            description='This is a test project',
            github_url='https://github.com/test/test1',
            live_url='https://test1.com',
        )
        self.project1.tags.add(self.tag_python)

        self.project2 = Project.objects.create(
            title='Test Project 2',
            description='This is a test project',
        )
        self.project2.tags.add(self.tag_django)

        self.project3 = Project.objects.create(
            title='Test Project 3',
            description='This has both tags',
        )
        self.project3.tags.set([self.tag_python, self.tag_django])

    def test_project_list_view_status_code(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertEqual(response.status_code, 200)

    def test_project_list_view_contains_correct_html(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_list_view_contains_all_projects(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertContains(response, self.project1.title)
        self.assertContains(response, self.project2.title)
        self.assertContains(response, self.project3.title)

    def test_project_list_view_empty(self):
        Project.objects.all().delete()
        response = self.client.get(reverse('projects:project_list'))
        self.assertContains(response, 'No projects found.')

    def test_project_list_filter_by_single_tag(self):
        response = self.client.get(f"{reverse('projects:project_list')}?tags={self.tag_python.id}")
        self.assertContains(response, self.project1.title)
        self.assertContains(response, self.project3.title)
        self.assertNotContains(response, self.project2.title)

    def test_project_list_filter_by_multiple_tags(self):
        response = self.client.get(
            f"{reverse('projects:project_list')}?tags={self.tag_python.id}&tags={self.tag_django.id}"
        )
        self.assertContains(response, self.project3.title)

    def test_project_list_context_data(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertIn('projects', response.context)
        self.assertIn('all_tags', response.context)
        self.assertIn('active_tags', response.context)

    def test_project_list_active_tags(self):
        response = self.client.get(f"{reverse('projects:project_list')}?tags={self.tag_python.id}")
        self.assertIn(self.tag_python, response.context['active_tags'])


class TestProjectDetailViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag = Tag.objects.create(name='Python')
        self.project = Project.objects.create(
            title='Test Project',
            description='This is a test project',
            github_url='https://github.com/test/test',
            live_url='https://test.com',
        )
        self.project.tags.add(self.tag)

    def test_project_detail_view_status_code(self):
        response = self.client.get(reverse('projects:project_detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_view_404(self):
        response = self.client.get(reverse('projects:project_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_project_detail_view_template(self):
        response = self.client.get(reverse('projects:project_detail', args=[self.project.id]))
        self.assertTemplateUsed(response, 'projects/project_detail.html')

    def test_project_detail_context_data(self):
        response = self.client.get(reverse('projects:project_detail', args=[self.project.id]))
        self.assertEqual(response.context['project'], self.project)

    def test_project_detail_content(self):
        response = self.client.get(reverse('projects:project_detail', args=[self.project.id]))
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.github_url)
        self.assertContains(response, self.project.live_url)
        self.assertContains(response, self.tag.name)
