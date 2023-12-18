# Generated by Django 3.2.23 on 2023-11-28 14:36

from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0003_cleanup_urls"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="cosign_confirmation_email_sent",
            field=models.BooleanField(
                default=False,
                help_text="Has the confirmation email been sent after the submission has successfully been cosigned?",
                verbose_name="cosign confirmation email sent",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="cosign_request_email_sent",
            field=models.BooleanField(
                default=False,
                help_text="Has the email to request a co-sign been sent?",
                verbose_name="cosign request email sent",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="payment_complete_confirmation_email_sent",
            field=models.BooleanField(
                default=False,
                help_text="Has the confirmation emails been sent after successful payment?",
                verbose_name="payment complete confirmation email sent",
            ),
        ),
        migrations.CreateModel(
            name="PostCompletionMetadata",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tasks_ids",
                    django_better_admin_arrayfield.models.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True, max_length=255, verbose_name="celery task ID"
                        ),
                        blank=True,
                        default=list,
                        help_text="Celery task IDs of the tasks queued once a post submission event happens.",
                        size=None,
                        verbose_name="task IDs",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(auto_now_add=True, verbose_name="created on"),
                ),
                (
                    "trigger_event",
                    models.CharField(
                        choices=[
                            ("on_completion", "On completion"),
                            ("on_payment_complete", "On payment complete"),
                            ("on_cosign_complete", "On cosign complete"),
                            ("on_retry", "On retry"),
                        ],
                        help_text="Which event scheduled these tasks.",
                        max_length=100,
                        verbose_name="created by",
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        help_text="Submission to which the result belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="submissions.submission",
                        verbose_name="submission",
                    ),
                ),
            ],
            options={
                "verbose_name": "post completion metadata",
                "verbose_name_plural": "post completion metadata",
            },
        ),
        migrations.AddConstraint(
            model_name="postcompletionmetadata",
            constraint=models.UniqueConstraint(
                condition=models.Q(("trigger_event", "on_completion")),
                fields=("submission",),
                name="unique_on_completion_event",
            ),
        ),
    ]