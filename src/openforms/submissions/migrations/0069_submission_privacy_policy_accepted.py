# Generated by Django 3.2.17 on 2023-02-03 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0068_merge_20221107_1647"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="privacy_policy_accepted",
            field=models.BooleanField(
                default=False,
                help_text="Has the user accepted the privacy policy?",
                verbose_name="privacy policy accepted",
            ),
        ),
    ]
