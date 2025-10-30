from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import CustomUser


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="Test course", description="Test courese", owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            title="Test lesson",
            description="Test lesson",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):

        url = reverse("lms:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("id"), self.lesson.pk)
        self.assertEqual(data.get("description"), self.lesson.description)

    def test_lesson_create(self):
        url = reverse("lms:lessons_create")
        data = {
            "title": "Python lessons",
            "description": "Python as pro",
            "video_link": "https://www.youtube.com/watch?v=wDmPgXhlDIg",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title="Python lessons").exists())
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lessons_update", args=(self.lesson.pk,))
        data = {
            "title": "Java lessons",
            "description": "Java as pro",
            "video_link": "https://www.youtube.com/watch?v=xTtL8E4LzTQ",
            "course": self.course.id,
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Java lessons")

    def test_lesson_delete(self):
        url = reverse("lms:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test1@test.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test course", owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            description="Test lesson",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("title"), self.course.title)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test1@test1.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test course", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_is_subscribed(self):
        url = reverse("users:subscribe")
        data = {
            "user": self.user,
            "course": self.course.id,
            "subscribed_at": "19-10-2025",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
