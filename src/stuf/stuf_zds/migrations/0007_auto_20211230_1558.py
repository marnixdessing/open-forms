# Generated by Django 2.2.25 on 2021-12-30 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stuf_zds", "0006_auto_20211001_1300"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stufzdsconfig",
            name="zds_documenttype_omschrijving",
        ),
        migrations.RemoveField(
            model_name="stufzdsconfig",
            name="zds_zaaktype_code",
        ),
        migrations.RemoveField(
            model_name="stufzdsconfig",
            name="zds_zaaktype_omschrijving",
        ),
        migrations.RemoveField(
            model_name="stufzdsconfig",
            name="zds_zaaktype_status_code",
        ),
        migrations.RemoveField(
            model_name="stufzdsconfig",
            name="zds_zaaktype_status_omschrijving",
        ),
    ]