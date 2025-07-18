from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import Order


@shared_task(bind=True, max_retries=3)
def order_created(self, order_id):
    try:
        order = Order.objects.select_related('coupon').get(id=order_id)

        subject = _('Order #%(order_id)s') % {'order_id': order.id}


        context = {
            'order': order,
            'items': order.items.select_related('book'),
            'coupon': order.coupon,
            'discount': order.discount,
        }

        text_content = render_to_string('orders/email/order_created.txt', context)
        html_content = render_to_string('orders/email/order_created.html', context)

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            cc=[settings.ORDER_NOTIFICATION_EMAIL] if hasattr(settings, 'ORDER_NOTIFICATION_EMAIL') else None
        )
        msg.attach_alternative(html_content, "text/html")

        result = msg.send()

        return {
            'status': 'success',
            'order_id': order.id,
            'email_sent_to': order.email,
            'retries': self.request.retries
        }

    except Order.DoesNotExist as exc:
        raise self.retry(exc=exc, countdown=60 * 2)  # Retry after 2 minutes

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * 5)  # Retry after 5 minutes


@shared_task
def order_payment_confirmed(order_id):
    order = Order.objects.get(id=order_id)

    subject = _('Payment confirmation for order #%(order_id)s') % {'order_id': order.id}

    context = {
        'order': order,
        'payment_date': order.updated,
    }

    text_content = render_to_string('orders/email/payment_confirmed.txt', context)
    html_content = render_to_string('orders/email/payment_confirmed.html', context)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )
    msg.attach_alternative(html_content, "text/html")

    return msg.send()