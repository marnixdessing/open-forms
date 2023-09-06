# Generated by Django 3.2.20 on 2023-09-05 10:49
from django.db import migrations


def strip_v1_suffix(apps, _):
    QmaticConfig = apps.get_model("qmatic", "QmaticConfig")
    config = QmaticConfig.objects.first()
    if config is None or not config.service:
        return

    # zgw-consumers normalizes api_root to add a trailing slash
    if not (base := config.service.api_root).endswith("/v1/"):
        return

    head, _ = base.rsplit("v1", 1)
    config.service.api_root = head
    config.service.save()


def readd_v1_suffix(apps, _):
    QmaticConfig = apps.get_model("qmatic", "QmaticConfig")
    config = QmaticConfig.objects.first()
    if config is None or not config.service:
        return

    if (base := config.service.api_root).endswith("/v1/"):
        return

    # zgw-consumers normalizes api_root to add a trailing slash
    config.service.api_root = f"{base}v1/"
    config.service.save()


class Migration(migrations.Migration):

    dependencies = [
        ("qmatic", "0002_qmaticconfig_required_customer_fields"),
    ]

    operations = [migrations.RunPython(strip_v1_suffix, readd_v1_suffix)]
