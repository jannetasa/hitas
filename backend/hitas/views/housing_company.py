import datetime
from collections import defaultdict
from typing import Any, Dict, List, Optional

from django.db.models import Min
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from hitas.exceptions import HousingCompanyNotFound
from hitas.models import Building, HousingCompany, PropertyManager, RealEstate
from hitas.views.codes import BuildingTypeSerializer, DeveloperSerializer, FinancingMethodSerializer
from hitas.views.helpers import Address, HitasModelViewSet, address_obj, value_or_none


class BuildingSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    building_identifier = serializers.SerializerMethodField()

    def get_address(self, obj: Building) -> Address:
        return address_obj(obj)

    def get_building_identifier(self, obj: Building) -> Optional[str]:
        return value_or_none(obj.building_identifier)

    class Meta:
        model = Building
        fields = [
            "address",
            "building_identifier",
            "completion_date",
        ]


class RealEstateSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    buildings = BuildingSerializer(many=True)

    def get_address(self, obj: RealEstate) -> Address:
        return address_obj(obj)

    class Meta:
        model = RealEstate
        fields = [
            "address",
            "property_identifier",
            "buildings",
        ]


class HousingCompanyListSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField(source="display_name", max_length=1024)
    state = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_id(self, obj: HousingCompany) -> str:
        return obj.uuid.hex

    def get_state(self, obj: HousingCompany) -> str:
        return obj.state.name.lower()

    def get_address(self, obj: HousingCompany) -> Address:
        return address_obj(obj)

    def get_area(self, obj: HousingCompany) -> Dict[str, Any]:
        return {"name": obj.postal_code.description, "cost_area": obj.area}

    def get_date(self, obj: HousingCompany) -> datetime.date:
        return obj.date

    class Meta:
        model = HousingCompany
        fields = ["id", "name", "state", "address", "area", "date"]


class PropertyManagerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, obj: Building) -> Address:
        return address_obj(obj)

    class Meta:
        model = PropertyManager
        fields = [
            "address",
            "name",
            "email",
        ]


class HousingCompanyDetailSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    real_estates = serializers.SerializerMethodField()
    building_type = serializers.SerializerMethodField()
    financing_method = serializers.SerializerMethodField()
    developer = serializers.SerializerMethodField()
    property_manager = PropertyManagerSerializer()
    acquisition_price = serializers.SerializerMethodField()
    last_modified = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    legacy_id = serializers.SerializerMethodField()

    def get_id(self, obj: HousingCompany) -> str:
        return obj.uuid.hex

    def get_name(self, obj: HousingCompany) -> Dict[str, str]:
        return {
            "display": obj.display_name,
            "official": obj.official_name,
        }

    def get_legacy_id(self, obj: HousingCompany) -> Optional[str]:
        return value_or_none(obj.legacy_id)

    def get_notes(self, obj: HousingCompany) -> Optional[str]:
        return value_or_none(obj.notes)

    def get_state(self, obj: HousingCompany) -> str:
        return obj.state.name.lower()

    def get_address(self, obj: HousingCompany) -> Address:
        return address_obj(obj)

    def get_area(self, obj: HousingCompany) -> Dict[str, any]:
        return {"name": obj.postal_code.description, "cost_area": obj.area}

    def get_date(self, obj: HousingCompany) -> datetime.date:
        return obj.date

    def get_building_type(self, obj: HousingCompany) -> Dict[str, Any]:
        return BuildingTypeSerializer(obj.building_type).data

    def get_financing_method(self, obj: HousingCompany) -> Dict[str, Any]:
        return FinancingMethodSerializer(obj.financing_method).data

    def get_developer(self, obj: HousingCompany) -> Dict[str, Any]:
        return DeveloperSerializer(obj.developer).data

    def get_acquisition_price(self, obj: HousingCompany) -> Dict[str, float]:
        return {
            "initial": obj.acquisition_price,
            "realized": obj.realized_acquisition_price,
        }

    def get_last_modified(self, obj: HousingCompany) -> Dict[str, Any]:
        return {
            "user": {
                "username": obj.last_modified_by.username,
                "first_name": value_or_none(obj.last_modified_by.first_name),
                "last_name": value_or_none(obj.last_modified_by.last_name),
            },
            "datetime": obj.last_modified_datetime,
        }

    def get_real_estates(self, obj: HousingCompany) -> List[Dict[str, Any]]:
        # Select all buildings for this housing company with one query instead
        # of having one query per property
        buildings_by_real_estate = defaultdict(list)
        for b in (
            Building.objects.select_related("postal_code")
            .only(
                "street_address",
                "postal_code__value",
                "building_identifier",
                "real_estate__id",
                "completion_date",
            )
            .filter(real_estate__housing_company_id=obj.id)
        ):
            buildings_by_real_estate[b.real_estate_id].append(b)

        # Fetch real estates
        query = obj.real_estates.select_related("postal_code").only(
            "street_address",
            "postal_code__value",
            "property_identifier",
            "housing_company__id",
        )

        return RealEstateSerializer(query.all(), context={"buildings": buildings_by_real_estate}, many=True).data

    class Meta:
        model = HousingCompany
        fields = [
            "id",
            "business_id",
            "name",
            "state",
            "address",
            "area",
            "date",
            "real_estates",
            "financing_method",
            "building_type",
            "developer",
            "property_manager",
            "acquisition_price",
            "primary_loan",
            "sales_price_catalogue_confirmation_date",
            "notification_date",
            "legacy_id",
            "notes",
            "last_modified",
        ]


class HousingCompanyViewSet(HitasModelViewSet):
    serializer_class = HousingCompanyDetailSerializer
    list_serializer_class = HousingCompanyListSerializer
    not_found_exception_class = HousingCompanyNotFound

    def get_list_queryset(self):
        return (
            HousingCompany.objects.select_related(
                "postal_code",
            )
            .annotate(date=Min("real_estates__buildings__completion_date"))
            .only("uuid", "state", "postal_code__value", "postal_code__description", "display_name", "street_address")
            .order_by("id")
        )

    def get_detail_queryset(self):
        return (
            HousingCompany.objects.select_related(
                "postal_code",
                "financing_method",
                "developer",
                "building_type",
                "property_manager",
                "property_manager__postal_code",
                "last_modified_by",
            )
            .annotate(date=Min("real_estates__buildings__completion_date"))
            .only(
                "uuid",
                "state",
                "postal_code__value",
                "postal_code__description",
                "financing_method__value",
                "financing_method__description",
                "financing_method__legacy_code_number",
                "developer__value",
                "developer__description",
                "developer__legacy_code_number",
                "building_type__value",
                "building_type__description",
                "building_type__legacy_code_number",
                "property_manager__name",
                "property_manager__email",
                "property_manager__street_address",
                "property_manager__postal_code__value",
                "property_manager__postal_code__description",
                "display_name",
                "street_address",
                "business_id",
                "official_name",
                "acquisition_price",
                "realized_acquisition_price",
                "primary_loan",
                "sales_price_catalogue_confirmation_date",
                "notification_date",
                "legacy_id",
                "notes",
                "last_modified_by__username",
                "last_modified_by__first_name",
                "last_modified_by__last_name",
                "last_modified_datetime",
            )
        )
