from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from net_coverage.models import ProvidersCoverage
from net_coverage.data.provider_codes import PROVIDERS


class ProviderNameFilter(admin.SimpleListFilter):
    title = _('provider_name')

    parameter_name = 'provider_name'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return PROVIDERS

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            queryset = queryset.filter(
                provider_mnc__in=[key for key, value in dict(PROVIDERS).items()
                                  if value == dict(PROVIDERS)[int(self.value())]],
            )
        return queryset


@admin.register(ProvidersCoverage)
class ProvidersCoverageAdmin(admin.ModelAdmin):
    list_display = [
        'get_provider_name', 'latitude', 'longitude', 'city_code', 'post_code',
        'two_g', 'three_g', 'four_g']
    search_fields = ['post_code', 'city_code']
    list_filter = [ProviderNameFilter, 'post_code', 'city_code', 'two_g', 'three_g', 'four_g']

    @admin.display(description='Provider Name')
    def get_provider_name(self, obj):
        if obj.provider_mnc:
            return dict(PROVIDERS)[obj.provider_mnc]
        else:
            return ""

