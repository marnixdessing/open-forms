from django.utils.translation import gettext_lazy as _

from drf_spectacular.plumbing import build_basic_type, build_object_type

STR_TYPE = build_basic_type(str)
assert STR_TYPE is not None
BOOL_TYPE = build_basic_type(bool)
assert BOOL_TYPE is not None

DECLARATION_SCHEMA = build_object_type(
    title=_("Declaration checkbox"),
    description=_(
        "A single Form.io checkbox component for the declarations that a user may have to accept before submitting a form."
    ),
    properties={
        "type": {
            **STR_TYPE,
            "description": _("Component type (checkbox)"),
        },
        "key": {
            **STR_TYPE,
            "description": _("Key of the declaration"),
        },
        "label": {
            **STR_TYPE,
            "description": _("Text of the declaration"),
        },
        "validate": build_object_type(
            properties={
                "required": {
                    **BOOL_TYPE,
                    "description": _(
                        "Whether accepting this declaration is required or not."
                    ),
                }
            }
        ),
    },
)
