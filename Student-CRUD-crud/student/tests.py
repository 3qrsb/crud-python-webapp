from django.test import TestCase
from django.urls import reverse
from student.models import Student

class StudentViewsTestCase(TestCase):

    def setUp(self):
        # Create a sample student for testing
        self.student = Student.objects.create(name='John', section='A', age=20)

    def test_student_list_view(self):
        response = self.client.get(reverse('student:student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_list.html')

    def test_student_create_view(self):
        data = {'name': 'Alice', 'section': 'B', 'age': 22}
        response = self.client.post(reverse('student:student_new'), data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(Student.objects.count(), 2)  # Assuming one student already exists

    def test_student_update_view(self):
        updated_data = {'name': 'Updated Name', 'section': 'C', 'age': 25}
        response = self.client.post(reverse('student:student_edit', args=[self.student.pk]), updated_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Updated Name')
        self.assertEqual(self.student.section, 'C')
        self.assertEqual(self.student.age, 25)

    def test_student_delete_view(self):
        response = self.client.post(reverse('student:student_delete', args=[self.student.pk]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
