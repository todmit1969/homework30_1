from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework import status
from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import PaymentSerializer


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

