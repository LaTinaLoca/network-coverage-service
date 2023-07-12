# Models for Network Coverage Service
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from net_coverage.data.provider_codes import PROVIDERS


class ProvidersCoverage(models.Model):
    """
    This table stores information about the provider (provider_mnc, i.e. Mobile Network Code),
    the lambert93 coordinates as well as the GPS latitude and longitude
    on the French territory. It adds the city code and the post code information (ints)
    together with the 2G/3G/4G network coverage (booleans).
    """

    provider_mnc = models.IntegerField(
        help_text="Mobile Network Code of a given network provider",
        choices=PROVIDERS
    )
    x = models.IntegerField(
        help_text="lambert93 x coordinate"
    )
    y = models.IntegerField(
        help_text="lambert93 y coordinate"
    )
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    city_code = models.IntegerField(
        help_text="citycode of the given latitude and longitude point",
        blank=True,
        null=True
    )
    post_code = models.IntegerField(
        help_text="postcode (it includes the city_code) of the given latitude and longitude point",
        blank=True,
        null=True
    )
    two_g = models.BooleanField(default=False)
    three_g = models.BooleanField(default=False)
    four_g = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Provider coverage for {dict(PROVIDERS)[self.provider_mnc]} with coordinates lat {self.latitude}" \
               f" and long {self.longitude}"
