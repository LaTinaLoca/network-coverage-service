from rest_framework import serializers
from net_coverage.models import ProvidersCoverage

class CoverageSerializer(serializers.Serializer):
    two_g = serializers.BooleanField()
    three_g = serializers.BooleanField()
    four_g = serializers.BooleanField()


class GetNetworkCoverageSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255)  # TODO: review the provider's name length
    coverage = CoverageSerializer()


class ProvidersCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvidersCoverage
        fields = '__all__'
