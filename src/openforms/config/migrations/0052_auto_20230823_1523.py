# Generated by Django 3.2.20 on 2023-08-23 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0051_auto_20230811_1217"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="enable_new_appointments",
        ),
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="enable_service_fetch",
        ),
    ]
