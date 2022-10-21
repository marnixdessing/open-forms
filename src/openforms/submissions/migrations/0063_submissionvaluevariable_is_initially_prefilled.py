# Generated by Django 3.2.16 on 2022-10-20 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # XXX: on master, this migration has a different dependency.
        # Users on stable/2.0.x upgrading to a newer version might have issues, see
        # https://github.com/open-formulieren/open-forms/issues/2224
        ("submissions", "0060_auto_20220812_1439"),
    ]

    operations = [
        migrations.AddField(
            model_name="submissionvaluevariable",
            name="is_initially_prefilled",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="Can this variable be prefilled at the beginning of a submission?",
                null=True,
                verbose_name="is initially prefilled",
            ),
        ),
    ]
