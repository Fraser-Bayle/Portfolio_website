from django.test import TestCase
from projects.models import Project, Tag
from django.core.exceptions import ValidationError


class TestProjectModels(TestCase):
    def setUp(self):
        # Create tag first
        self.tag_python = Tag.objects.create(name='Python')

        # Create project
        self.project = Project.objects.create(
            title='Test Project',
            description='This is a test project',
            github_url='https://github.com/test/test',
            live_url='https://test.com',
        )
        # Add tag using ID
        self.project.tags.add(self.tag_python.id)

    def test_project_str(self):
        self.assertEqual(str(self.project), self.project.title)

    def test_project_has_tags(self):
        self.assertEqual(self.project.tags.count(), 1)

    def test_project_has_tag(self):
        self.assertEqual(self.project.tags.first().name, 'Python')

    def test_project_creation_requires_name(self):
        with self.assertRaises(Exception):
            Project.objects.create(description='No title provided')

    def test_project_creation_requires_description(self):
        with self.assertRaises(Exception):
            Project.objects.create(title='Test Project')

    def test_project_optional_fields(self):
        project = Project.objects.create(
            title='Optional Fields Test',
            description='Testing optional fields'
        )
        self.assertIsNone(project.live_url)
        self.assertIsNone(project.github_url)
        self.assertFalse(bool(project.thumbnail))
        self.assertIsNone(project.image)

    def test_project_created_at_auto_now(self):
        self.assertIsNotNone(self.project.created_at)

    def test_project_multiple_tags(self):
        tag_django = Tag.objects.create(name='Django')
        self.project.tags.add(tag_django)
        self.assertEqual(self.project.tags.count(), 2)
        self.assertIn(self.tag_python, self.project.tags.all())
        self.assertIn(tag_django, self.project.tags.all())


class TestTagModels(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Python')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'Python')

    def test_tag_name_unique(self):
        with self.assertRaises(Exception):
            Tag.objects.create(name='Python')

    def test_tag_name_max_length(self):
        with self.assertRaises(ValidationError):
            tag = Tag(name='x' * 51)
            tag.full_clean()  # This will validate the model

    def test_tag_projects_relation(self):
        project = Project.objects.create(
            title='Test Project',
            description='Test Description'
        )
        project.tags.add(self.tag)
        self.assertEqual(self.tag.projects.count(), 1)
        self.assertEqual(self.tag.projects.first(), project)
