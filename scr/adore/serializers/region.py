from rest_framework.serializers import ModelSerializer

from scr.adore.models.region import *


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'region')


class MahallaModelSerializer(ModelSerializer):
    class Meta:
        model = Mahalla
        fields = ('id', 'name', 'district')


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'mahalla', 'street', 'house')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'region': instance.mahalla.district.region.name,
            'district': instance.mahalla.district.name,
            'mahalla': instance.mahalla.name,
            'street': instance.street,
            'house': instance.house
        }
