# Generated by Django 2.2.20 on 2021-05-21 11:52

from django.db import migrations, models

import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0003_auto_20210514_1453"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="globalconfiguration",
            options={"verbose_name": "General configuration"},
        ),
        migrations.AlterField(
            model_name="globalconfiguration",
            name="email_template_netloc_allowlist",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.CharField(max_length=1000),
                blank=True,
                default=list,
                help_text="Provide a list of allowed domains (without 'https://www').Hyperlinks in a (confirmation) email are removed, unless the domain is provided here.",
                size=None,
                verbose_name="allowed email domain names",
            ),
        ),
    ]
