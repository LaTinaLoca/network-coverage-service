from rest_framework import serializers


class CoverageSerializer(serializers.Serializer):
    twoG = serializers.BooleanField()
    threeG = serializers.BooleanField()
    fourG = serializers.BooleanField()


class GetNetworkCoverageSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255)  # TODO: review the provider's name length
    coverage = CoverageSerializer()
