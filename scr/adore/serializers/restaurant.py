from rest_framework import serializers
from rest_framework.serializers import *

from scr.adore.models.booking import Time
from scr.adore.models.region import Address
from scr.adore.models.restaurant import *
from scr.adore.serializers.booking import RestaurantCommentSerializer, TimeSerializer
from scr.adore.serializers.region import AddressSerializer
from scr.user.serializers import UserModelSerializer


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class MultipleImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        restaurant = validated_data.pop('restaurant')

        images = []
        for image_data in images_data:
            images.append(Image(image=image_data, restaurant=restaurant))

        return Image.objects.bulk_create(images)


class RestaurantImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'restaurant')


class ServiceModelSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'image')


class ServiceRestaurantSerializer(ModelSerializer):
    class Meta:
        model = ServiceRestaurant
        fields = ('service',)


class RestaurantModelSerializer(ModelSerializer):
    address = AddressSerializer()
    working_time = TimeSerializer()
    services = PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'price', 'description', 'phone', 'size_people', 'address', 'user', 'services', 'working_time')

    def validate(self, attrs):
        if attrs.get('size_people') < 1:
            raise ValidationError("Size people must be greater than 0")

        if attrs.get('price') < 1:
            raise ValidationError("Price must be greater than 0")

        if attrs.get('phone') is not None and len(attrs.get('phone')) < 9:
            raise ValidationError("Phone number must be at least 9 characters")

        if attrs.get('working_time') is not None:
            morning_time = attrs.get('working_time').get('morning_time')
            afternoon_time = attrs.get('working_time').get('afternoon_time')
            evening_time = attrs.get('working_time').get('evening_time')

            if morning_time is None or afternoon_time is None or evening_time is None:
                raise ValidationError("All working time fields are required")

            if len(morning_time) < 5 or len(afternoon_time) < 5 or len(evening_time) < 5:
                raise ValidationError("Invalid time format")

            if not morning_time[2] == ':' or not afternoon_time[2] == ':' or not evening_time[2] == ':':
                raise ValidationError("Invalid time format")

        if attrs.get('services') is not None:
            services = attrs.get('services')
            if len(services) < 1:
                raise ValidationError("At least one service is required")

        if attrs.get('images') is not None:
            images = attrs.get('images')
            if len(images) < 1:
                raise ValidationError("At least one image is required")

        if attrs.get('address') is not None:
            address = attrs.get('address')
            if address.get('mahalla') is None:
                raise ValidationError("Mahalla is required")

        return attrs

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        services_data = validated_data.pop('services')
        working_time_data = validated_data.pop('working_time', None)

        address = Address.objects.create(**address_data)
        restaurant = Restaurant.objects.create(address=address, **validated_data)
        restaurant.save()

        if working_time_data:
            working_time = Time.objects.create(restaurant=restaurant, **working_time_data)
            restaurant.working_time = working_time
            restaurant.save()

        for service_data in services_data:
            restaurant.services.add(service_data)

        return restaurant

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        services_data = validated_data.pop('services', None)
        working_time_data = validated_data.pop('working_time', None)

        if address_data is not None:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        if working_time_data is not None:
            instance.working_time = working_time_data
            instance.save()

        if services_data is not None:
            instance.services.set(services_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class RestaurantListSerializer(ModelSerializer):
    address = AddressSerializer()
    images = ImageModelSerializer(many=True, source='restaurant_images')

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'price', 'description', 'size_people', 'images', 'address')


class MyRestaurantListSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'price', 'phone', 'size_people', 'address')


class RestaurantDetailModelSerializer(ModelSerializer):
    address = AddressSerializer()
    services = PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    user = UserModelSerializer()
    comments = RestaurantCommentSerializer(many=True)
    comment_count = SerializerMethodField()
    images = ImageModelSerializer(many=True, source='restaurant_images')
    working_time = TimeSerializer(source='time', many=True)

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'price', 'description', 'phone', 'size_people', 'images', 'address', 'services', 'user',
            'comments', 'comment_count', 'working_time')

    def get_comment_count(self, obj):
        return obj.comments.count()
