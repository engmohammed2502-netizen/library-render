"""
اختبارات أساسية للتطبيق.
الهدف: التأكد إن الصفحات الرئيسية بتفتح صح، وإن نظام الصلاحيات
(ROOT / ADMIN / STUDENT) شغال زي ما هو متوقع بالظبط.

يشتغل بالأمر:
    python manage.py test
"""

from django.test import TestCase
from django.urls import reverse
from .models import User, Course


class PublicPagesTests(TestCase):
    """اختبارات الصفحات المتاحة بدون تسجيل دخول."""

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_guest_login_page_loads(self):
        response = self.client.get(reverse('guest_login'))
        self.assertEqual(response.status_code, 200)

    def test_home_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_credentials_shows_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent_user',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(
            any('غير صحيحة' in str(m) for m in messages_list),
            "المفروض تظهر رسالة خطأ لما بيانات الدخول تكون غلط"
        )


class AuthenticatedPagesTests(TestCase):
    """اختبارات الصفحات اللي محتاجة تسجيل دخول، وفحص الصلاحيات."""

    def setUp(self):
        self.student = User.objects.create_user(
            username='student1', password='testpass123',
            full_name='Test Student', user_type='STUDENT'
        )
        self.professor = User.objects.create_user(
            username='prof1', password='testpass123',
            full_name='Test Professor', user_type='ADMIN'
        )
        self.root = User.objects.create_user(
            username='root1', password='testpass123',
            full_name='Test Root', user_type='ROOT',
            is_staff=True, is_superuser=True
        )
        self.course = Course.objects.create(
            name='Test Course', code='TST101',
            department='ELEC', semester=1,
            professor=self.professor
        )

    # --- فحص إن الصفحات الأساسية بتفتح ---

    def test_home_loads_for_logged_in_user(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_department_page_loads(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('department', args=['ELEC']))
        self.assertEqual(response.status_code, 200)

    def test_semester_page_loads_and_shows_course(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('semester', args=['ELEC', 1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_course_detail_page_loads(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)

    # --- فحص الصلاحيات: زر إضافة كورس ---

    def test_student_does_not_see_add_course_button(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('semester', args=['ELEC', 1]))
        self.assertNotContains(response, 'addCourseModal')

    def test_professor_sees_add_course_button(self):
        self.client.login(username='prof1', password='testpass123')
        response = self.client.get(reverse('semester', args=['ELEC', 1]))
        self.assertContains(response, 'addCourseModal')

    # --- فحص الصلاحيات: إضافة كورس فعلياً ---

    def test_professor_can_add_course(self):
        self.client.login(username='prof1', password='testpass123')
        response = self.client.post(reverse('add_course', args=['ELEC', 1]), {
            'name': 'New Course',
            'code': 'NEW202',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(code='NEW202').exists())

    def test_student_cannot_add_course(self):
        self.client.login(username='student1', password='testpass123')
        self.client.post(reverse('add_course', args=['ELEC', 1]), {
            'name': 'Hacked Course',
            'code': 'HACK1',
        })
        self.assertFalse(Course.objects.filter(code='HACK1').exists())

    # --- فحص الصلاحيات: لوحة تحكم الروت ---

    def test_professor_cannot_access_root_dashboard(self):
        self.client.login(username='prof1', password='testpass123')
        response = self.client.get(reverse('root_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_student_cannot_access_root_dashboard(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('root_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_root_can_access_dashboard(self):
        self.client.login(username='root1', password='testpass123')
        response = self.client.get(reverse('root_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_student_cannot_access_add_user_page(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('add_user'))
        self.assertEqual(response.status_code, 302)
