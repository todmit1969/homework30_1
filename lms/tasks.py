from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from lms.models import Course
from users.models import Subscription
from datetime import timedelta
from django.utils import timezone


@shared_task
def send_email(course_id=None):
    """ Рассылка писем пользователям при обновлении курса. """
    try:
        course = Course.objects.get(id=course_id)

        if timezone.now() - course.update_at >= timedelta(hours=4):
            subscriptions = Subscription.objects.filter(course=course)
            if subscriptions.exists():
                emails = [subscription.user.email for subscription in subscriptions]
                send_mail(
                    subject=f'Курс "{course.name}" обновлен',
                    message=f'Добрый день! Вы подписаны на обновление курса "{course.name}". Можете просмотреть '
                            f'изменения в личном кабинете.',
                    from_email= EMAIL_HOST_USER,
                    recipient_list=emails
                )
                print(f"Письма отправлены {len(emails)} подписчикам")
                return f"Уведомления отправлены для курса: {course.name} (ID: {course_id})"

            return f"Нет подписчиков на курс: {course.name} (ID: {course_id})"

            course.notification_task_id = None
            course.save()
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        send_email.retry(args=[course_id], kwargs={'delay_hours': 1}, exc=e, countdown=3600)