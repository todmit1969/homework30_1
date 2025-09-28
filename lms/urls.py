from rest_framework.routers import SimpleRouter
from django.urls import path

from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

from lms.apps import LmsConfig

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path('lms/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lms/<int:pk>', LessonRetrieveAPIView.as_view(),name='lessons_retrieve' ),
    path('lms/create', LessonCreateAPIView.as_view(),name='lessons_create'),
    path('lms/<int:pk>/delete', LessonDestroyAPIView.as_view(), name='lessons_delete'),
    path('lms/<int:pk>/update', LessonUpdateAPIView.as_view(),name='lessons_update'),

]

urlpatterns += router.urls
