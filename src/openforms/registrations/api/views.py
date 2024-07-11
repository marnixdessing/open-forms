from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from zgw_consumers.api_models.base import factory
from zgw_consumers.api_models.catalogi import Catalogus, InformatieObjectType

from openforms.api.views import ListMixin

from ..constants import RegistrationAttribute
from ..registry import register
from .filters import (
    APIGroupQueryParamsSerializer,
    ListInformatieObjectTypenQueryParamsSerializer,
)
from .serializers import (
    CatalogusSerializer,
    ChoiceWrapper,
    InformatieObjectTypeChoiceSerializer,
    RegistrationAttributeSerializer,
    RegistrationPluginSerializer,
)


@extend_schema_view(
    get=extend_schema(summary=_("List available registration plugins")),
)
class PluginListView(ListMixin, APIView):
    """
    List all available registration plugins.

    Registration plugins are responsible for the implementation details to register the form submission
    with various backends, such as "API's voor zaakgericht werken", StUF-ZDS and others.
    """

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = RegistrationPluginSerializer

    def get_objects(self):
        return list(register.iter_enabled_plugins())


@extend_schema_view(
    get=extend_schema(summary=_("List available registration attributes")),
)
class AllAttributesListView(ListMixin, APIView):
    """
    List the available registration attributes.
    """

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = RegistrationAttributeSerializer

    def get_objects(self):
        choices = RegistrationAttribute.choices

        return [ChoiceWrapper(choice) for choice in choices]


@extend_schema_view(
    get=extend_schema(
        summary=_("List available Catalogi"),
        parameters=[APIGroupQueryParamsSerializer],
    ),
)
class CatalogiListView(ListMixin, APIView):
    """
    List the available Catalogi based on the provided API group.
    """

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CatalogusSerializer

    def get_objects(self):
        filter_serializer = APIGroupQueryParamsSerializer(
            data=self.request.query_params
        )
        filter_serializer.is_valid(raise_exception=True)

        client = filter_serializer.get_ztc_client()
        if not client:
            return []

        catalogus_data = client.get_all_catalogi()
        return factory(Catalogus, catalogus_data)


@extend_schema_view(
    get=extend_schema(
        summary=_("List available InformatieObjectTypen"),
        parameters=[ListInformatieObjectTypenQueryParamsSerializer],
    ),
)
class InformatieObjectTypenListView(ListMixin, APIView):
    """
    List the available InformatieObjectTypen based on the configured registration backend and ZGW APIs services.

    Each InformatieObjectType is uniquely identified by its 'omschrijving', 'catalogus',
    and beginning and end date. If multiple same InformatieObjectTypen exist for different dates,
    only one entry is returned.
    """

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = InformatieObjectTypeChoiceSerializer

    def get_objects(self):
        filter_serializer = ListInformatieObjectTypenQueryParamsSerializer(
            data=self.request.query_params
        )
        filter_serializer.is_valid(raise_exception=True)

        client = filter_serializer.get_ztc_client()
        if not client:
            return []

        catalogus_data = client.get_all_catalogi()
        catalogus_mapping = {
            catalogus["url"]: catalogus for catalogus in catalogus_data
        }

        if "catalogus_domein" in filter_serializer.validated_data:
            domein = filter_serializer.validated_data["catalogus_domein"]
            # `catalogus_rsin` is guaranteed to be present if `catalogus_domein` is:
            rsin = filter_serializer.validated_data["catalogus_rsin"]

            matching_catalogus: str | None = next(
                (
                    catalogus["url"]
                    for catalogus in catalogus_data
                    if catalogus["domein"] == domein and catalogus["rsin"] == rsin
                ),
                None,
            )

            if matching_catalogus is None:
                return []

            iotypen_data = client.get_all_informatieobjecttypen(
                catalogus=matching_catalogus
            )
        else:
            iotypen_data = client.get_all_informatieobjecttypen()

        iotypen = []

        for iotype in iotypen_data:
            # fmt: off
            exists = any(
                existing_iotype["informatieobjecttype"].omschrijving == iotype["omschrijving"]
                and existing_iotype["informatieobjecttype"].catalogus == iotype["catalogus"]
                for existing_iotype in iotypen
            )
            # fmt: on

            if not exists:
                iotypen.append(
                    {
                        "informatieobjecttype": factory(InformatieObjectType, iotype),
                        "catalogus": factory(
                            Catalogus, catalogus_mapping[iotype["catalogus"]]
                        ),
                    }
                )

        return iotypen
