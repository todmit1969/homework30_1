from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from lms.models import Course, Lesson


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    number_phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    town = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="users", blank=True, null=True, verbose_name="Аватар пользователя"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты"
    )

    payment_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    paid_item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Платеж от {self.user} на сумму {self.amount} руб."

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
