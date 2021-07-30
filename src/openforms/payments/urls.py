from django.urls import path

from .views import PaymentReturnView, PaymentStartView, PaymentWebhookView

app_name = "payments"

urlpatterns = [
    path(
        "<uuid:uuid>/<slug:plugin_id>/start",
        PaymentStartView.as_view(),
        name="start",
    ),
    path(
        "<uuid:uuid>/return",
        PaymentReturnView.as_view(),
        name="return",
    ),
    path(
        "<slug:plugin_id>/webhook",
        PaymentWebhookView.as_view(),
        name="webhook",
    ),
]
