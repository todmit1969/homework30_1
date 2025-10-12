from django.contrib import admin

from users.models import Payment, CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email"
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "amount",
        "payment_method"
    )
