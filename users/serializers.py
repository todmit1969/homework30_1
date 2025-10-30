from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

from lms.models import Lesson, Course
from users.models import Payment, CustomUser, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['date', 'stripe_session_id', 'payment_url', 'user']

    def validate(self, data):
        payment_method = data.get('payment_method')
        course_id = self.context['request'].data.get('course')
        lesson_id = self.context['request'].data.get('lesson')

        if not course_id and not lesson_id:
            raise serializers.ValidationError("Укажите курс или урок")
        if course_id and lesson_id:
            raise serializers.ValidationError("Укажите только курс, или только урок!")

        if course_id:
            course = get_object_or_404(Course, id=course_id)
            if course.price <= 0:
                raise serializers.ValidationError("Цена курса должна быть больше нуля")
            data['course'] = course
            data['lesson'] = None
            data['amount'] = course.price
        elif lesson_id:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            if lesson.price <= 0:
                raise serializers.ValidationError("Цена урока должна быть больше нуля")
            data['lesson'] = lesson
            data['course'] = None
            data['amount'] = lesson.price

        if payment_method == 'stripe':
            if 'stripe_session_id' in data or 'payment_url' in data:
                raise serializers.ValidationError("Поля stripe_session_id и payment_url заполняются автоматически")
        else:
            data['stripe_session_id'] = None
            data['payment_url'] = None

        data['user'] = self.context['request'].user
        return data


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
