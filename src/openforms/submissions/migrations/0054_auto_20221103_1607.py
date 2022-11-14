# Generated by Django 3.2.15 on 2022-11-03 15:07

from django.db import migrations, models

import openforms.submissions.models.submission_step


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0002_auto_20210917_1114_squashed_0045_remove_formstep_optional"),
        ("submissions", "0001_initial_squashed_0057_alter_submissionvaluevariable_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="submissionstep",
            name="form_step_history",
            field=models.JSONField(
                blank=True,
                default=None,
                editable=False,
                encoder=openforms.submissions.models.submission_step.FrozenDjangoJSONEncoder,
                null=True,
                verbose_name="form step (historical)",
            ),
        ),
        migrations.AlterField(
            model_name="submissionstep",
            name="form_step",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=openforms.submissions.models.submission_step.RECORD_HISTORICAL_FORM_STEP,
                to="forms.formstep",
            ),
        ),
    ]