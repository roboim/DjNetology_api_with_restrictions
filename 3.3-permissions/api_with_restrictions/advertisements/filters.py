from django_filters import rest_framework as filters, DateFromToRangeFilter, FilterSet

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры

    class Meta:
        model = Advertisement


class F(FilterSet):
    updated_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['updated_at']