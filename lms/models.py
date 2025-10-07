from django.db import models
from django.db.models import CASCADE


class Course(models.Model):
    title = models.CharField(
        max_length=100, unique=True, blank=True, verbose_name="курс"
    )
    preview = models.ImageField(upload_to="lms/images", blank=True, null=True)
    description = models.TextField(max_length=200, verbose_name="описание")

    def __str__(self):
        return f"{self.title}, {self.description}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering =['title']

class Lesson(models.Model):
    title = models.CharField(
        max_length=100, unique=True, blank=True, verbose_name="урок"
    )
    preview = models.ImageField(upload_to="lms/images", blank=True, null=True)
    description = models.TextField(max_length=200, verbose_name="описание")
    video_link = models.CharField(
        max_length=100, unique=True, blank=True, null=True, verbose_name="ссылка"
    )
    course = models.ForeignKey(Course, on_delete=CASCADE, related_name="lessons")

    def __str__(self):
        return f"{self.title}, {self.description}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering =['title']
