from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework import status
from users.filters import PaymentFilter
from users.models import Payment, CustomUser
from users.serializers import PaymentSerializer, CustomUserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['date']
    ordering = ['-date']

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course")
        lesson_id = request.data.get("lesson")
        payment_method = request.data.get("payment_method")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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