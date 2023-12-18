# Generated by Django 3.2.23 on 2023-12-06 08:21

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import openforms.utils.fields


def global_theme_config_to_dedicated_model(apps, _):
    GlobalConfiguration = apps.get_model("config", "GlobalConfiguration")
    Theme = apps.get_model("config", "Theme")

    config = GlobalConfiguration.objects.first()
    if not config:
        return

    # if no styling things are configured, there's no point in creating a theme record
    if not any(
        [
            config.logo,
            config.theme_classname,
            config.theme_stylesheet,
            config.theme_stylesheet_file,
            config.design_token_values,
        ]
    ):
        return

    # create a theme record with the equivalent configuration and set it as default
    theme = Theme.objects.create(
        name="Standaard",
        logo=config.logo,
        classname=config.theme_classname,
        stylesheet=config.theme_stylesheet,
        stylesheet_file=config.theme_stylesheet_file,
        design_token_values=config.design_token_values,
    )
    config.default_theme = theme
    config.save()


def dedicated_model_to_global_configuration(apps, _):
    GlobalConfiguration = apps.get_model("config", "GlobalConfiguration")

    config = GlobalConfiguration.objects.first()
    if not config or not (theme := config.default_theme):
        return

    config.logo = theme.logo
    config.theme_classname = theme.classname
    config.theme_stylesheet = theme.stylesheet
    config.theme_stylesheet_file = theme.stylesheet_file
    config.design_token_values = theme.design_token_values
    config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0063_auto_20231122_1816"),
    ]

    operations = [
        migrations.CreateModel(
            name="Theme",
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
                    "name",
                    models.CharField(
                        help_text="An easily recognizable name for the theme, used to identify it.",
                        max_length=100,
                        verbose_name="name",
                    ),
                ),
                (
                    "logo",
                    openforms.utils.fields.SVGOrImageField(
                        blank=True,
                        help_text="Upload the theme/orgnization logo, visible to users filling out forms. We advise dimensions around 150px by 75px. SVG's are permitted.",
                        upload_to="logo/",
                        verbose_name="theme logo",
                    ),
                ),
                (
                    "classname",
                    models.SlugField(
                        blank=True,
                        help_text="If provided, this class name will be set on the <html> element.",
                        verbose_name="theme CSS class name",
                    ),
                ),
                (
                    "stylesheet",
                    models.URLField(
                        blank=True,
                        help_text="The URL stylesheet with theme-specific rules for your organization. This will be included as final stylesheet, overriding previously defined styles. Note that you also have to include the host to the `style-src` CSP directive. Example value: https://unpkg.com/@utrecht/design-tokens@1.0.0-alpha.20/dist/index.css.",
                        max_length=1000,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="The URL must point to a CSS resource (.css extension).",
                                regex="\\.css$",
                            )
                        ],
                        verbose_name="theme stylesheet URL",
                    ),
                ),
                (
                    "stylesheet_file",
                    models.FileField(
                        blank=True,
                        help_text="A stylesheet with theme-specific rules for your organization. This will be included as final stylesheet, overriding previously defined styles. If both a URL to a stylesheet and a stylesheet file have been configured, the uploaded file is included after the stylesheet URL.",
                        upload_to="config/themes/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=("css",)
                            )
                        ],
                        verbose_name="theme stylesheet",
                    ),
                ),
                (
                    "design_token_values",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Values of various style parameters, such as border radii, background colors... Note that this is advanced usage. Any available but un-specified values will use fallback default values. See https://open-forms.readthedocs.io/en/latest/installation/form_hosting.html#run-time-configuration for documentation.",
                        verbose_name="design token values",
                    ),
                ),
            ],
            options={
                "verbose_name": "theme",
                "verbose_name_plural": "themes",
            },
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="default_theme",
            field=models.OneToOneField(
                blank=True,
                help_text="If no explicit theme is configured, the configured default theme will be used as a fallback.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="config.theme",
                verbose_name="default theme",
            ),
        ),
        migrations.RunPython(
            code=global_theme_config_to_dedicated_model,
            reverse_code=dedicated_model_to_global_configuration,
        ),
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="design_token_values",
        ),
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="logo",
        ),
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="theme_classname",
        ),
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="theme_stylesheet",
        ),
        migrations.RemoveField(
            model_name="globalconfiguration",
            name="theme_stylesheet_file",
        ),
    ]