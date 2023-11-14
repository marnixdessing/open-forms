# Generated by Django 3.2.21 on 2023-11-09 08:58

from django.core.management import call_command
from django.db import migrations


def call_management_command(apps, schema_editor):
    call_command("create_csp_form_action_directives_from_config")


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0059_convert_button_design_tokens"),
        ("payments_ogone", "0002_auto_20210902_2120"),
        ("digid_eherkenning", "0006_digidconfiguration_metadata_file_source_and_more"),
    ]

    operations = [
        migrations.RunPython(call_management_command, migrations.RunPython.noop),
    ]