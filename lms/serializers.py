from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson
from lms.validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = VideoLinkValidator(field='video_link')


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    number_of_lessons = SerializerMethodField()

    def get_number_of_lessons(self, course):
        return Lesson.objects.filter(course =course).count()

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "lessons", "number_of_lessons")
