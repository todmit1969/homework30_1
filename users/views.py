import stripe
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course
from users.filters import PaymentFilter
from users.models import CustomUser, Payment, Subscription
from users.payment_service import (create_stripe_checkout_session,
                                   create_stripe_price, create_stripe_product)
from users.serializers import CustomUserSerializer, PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['date']
    ordering = ['-date']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Payment.objects.filter(user=self.request.user).select_related('user', 'course', 'lesson')
        return Payment.objects.none()

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course")
        lesson_id = request.data.get("lesson")
        payment_method = request.data.get("payment_method")

        if not self.request.user.is_authenticated:
            return Response({"error": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if payment_method == "stripe":
            try:
                validated_data = serializer.validated_data
                item = validated_data['course'] or validated_data['lesson']
                item_type = "course" if validated_data['course'] else "lesson"

                product_id = create_stripe_product(item.title)
                price_id = create_stripe_price(product_id, float(item.price))

                success_url = request.build_absolute_uri(
                    reverse('materials:course-detail' if item_type == "course"
                            else 'materials:lesson-detail',
                            kwargs={'pk': course_id or lesson_id})
                )
                cancel_url = success_url
                session_data = create_stripe_checkout_session(price_id, success_url, cancel_url)

#                payment = Payment.objects.create(
#                    user=validated_data['user'],
#                    course=validated_data['course'],
#                    lesson=validated_data['lesson'],
#                    amount=validated_data['amount'],
#                    payment_method="stripe",
#                    stripe_session_id=session_data["session_id"],
#                    payment_url=session_data["url"]
#                )
                return Response({"payment_url": session_data["url"]}, status=status.HTTP_201_CREATED)

            except stripe.error.StripeError as e:
                return Response({"error": f"Ошибка платежной системы: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": f"Внутренняя ошибка сервера: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CustomUser.objects.filter(id=self.request.user.id)
        return CustomUser.objects.none()


class SubscriptionView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
