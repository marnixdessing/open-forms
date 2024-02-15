from typing import Any

from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from openforms.formio.validators import variable_key_validator
from openforms.template.validators import DjangoTemplateValidator
from openforms.utils.mixins import JsonSchemaSerializerMixin
from openforms.utils.validators import validate_rsin


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Variable mapping example",
            value={
                "variable_key": "my_edit_grid.0.field",
                "target_path": ["path", "to.the", "target"],
            },
        )
    ]
)
class ObjecttypeVariableMappingSerializer(serializers.Serializer):
    """A mapping between a form variable key and the corresponding Objecttype JSON location."""

    variable_key = serializers.CharField(
        label=_("variable key"),
        help_text=_(
            "The 'dotted' path to a form variable key. The format should comply to how Formio handles nested component keys."
        ),
        validators=[variable_key_validator],
    )
    target_path = serializers.ListField(
        child=serializers.CharField(label=_("Part of a JSON path")),
        label=_("target path"),
        help_text=_(
            "Representation of the JSON target location as a list of string 'bits'."
        ),
    )


class ObjectsAPIOptionsSerializer(JsonSchemaSerializerMixin, serializers.Serializer):

    version = serializers.ChoiceField(
        label=_("options version"),
        help_text=_(
            "The schema version of the objects API Options. Not to be confused with the objecttype version."
        ),
        choices=[1, 2],
        default=1,
    )
    objecttype = serializers.URLField(
        label=_("objecttype"),
        help_text=_(
            "URL that points to the ProductAanvraag objecttype in the Objecttypes API. "
            "The objecttype should have the following three attributes: "
            "1) submission_id; "
            "2) type (the type of productaanvraag); "
            "3) data (the submitted form data)"
        ),
    )
    objecttype_version = serializers.IntegerField(
        label=_("objecttype version"),
        help_text=_("Version of the objecttype in the Objecttypes API"),
    )
    productaanvraag_type = serializers.CharField(
        label=_("productaanvraag type"),
        help_text=_("The type of ProductAanvraag"),
        required=False,
    )
    informatieobjecttype_submission_report = serializers.URLField(
        label=_("submission report PDF informatieobjecttype"),
        help_text=_(
            "URL that points to the INFORMATIEOBJECTTYPE in the Catalogi API "
            "to be used for the submission report PDF"
        ),
        required=False,
    )
    upload_submission_csv = serializers.BooleanField(
        label=_("Upload submission CSV"),
        help_text=_(
            "Indicates whether or not the submission CSV should be uploaded as "
            "a Document in Documenten API and attached to the ProductAanvraag"
        ),
        default=False,
    )
    informatieobjecttype_submission_csv = serializers.URLField(
        label=_("submission report CSV informatieobjecttype"),
        help_text=_(
            "URL that points to the INFORMATIEOBJECTTYPE in the Catalogi API "
            "to be used for the submission report CSV"
        ),
        required=False,
    )
    informatieobjecttype_attachment = serializers.URLField(
        label=_("attachment informatieobjecttype"),
        help_text=_(
            "URL that points to the INFORMATIEOBJECTTYPE in the Catalogi API "
            "to be used for the submission attachments"
        ),
        required=False,
    )
    organisatie_rsin = serializers.CharField(
        label=_("organisation RSIN"),
        validators=[validate_rsin],
        help_text=_("RSIN of organization, which creates the INFORMATIEOBJECT"),
        required=False,
    )

    # V1 only fields:
    content_json = serializers.CharField(
        label=_("JSON content field"),
        help_text=_(
            "JSON template for the body of the request sent to the Objects API."
        ),
        validators=[
            DjangoTemplateValidator(
                backend="openforms.template.openforms_backend",
            ),
        ],
        required=False,
    )
    payment_status_update_json = serializers.CharField(
        label=_("payment status update JSON template"),
        help_text=_(
            "This template is evaluated with the submission data and the resulting JSON is sent to the objects API "
            "with a PATCH to update the payment field."
        ),
        validators=[
            DjangoTemplateValidator(
                backend="openforms.template.openforms_backend",
            ),
        ],
        required=False,
    )

    # V2 only fields:
    variables_mapping = ObjecttypeVariableMappingSerializer(
        label=_("variables mapping"),
        many=True,
        required=False,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        v1_only_fields = {"content_json", "payment_status_update_json"}
        v2_only_fields = {"variables_mapping"}

        version = attrs["version"]

        if version == 1:
            v1_forbidden_fields = v2_only_fields.intersection(attrs)
            if v1_forbidden_fields:
                raise ValidationError(
                    {
                        k: _(
                            "{field_name} shouldn't be provided when version is 1"
                        ).format(field_name=k)
                        for k in v1_forbidden_fields
                    }
                )
        if version == 2:
            v2_forbidden_fields = v1_only_fields.intersection(attrs)
            if v2_forbidden_fields:
                raise ValidationError(
                    {
                        k: _(
                            "{field_name} shouldn't be provided when version is 2"
                        ).format(field_name=k)
                        for k in v2_forbidden_fields
                    }
                )

        return attrs
