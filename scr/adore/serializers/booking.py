from datetime import date

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework.serializers import *

from root import settings
from scr.adore.models.booking import *
from scr.adore.models.restaurant import Restaurant
from scr.user.serializers import UserCommentSerializer, UserModelSerializer


class CommentSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', 'restaurant', 'created_at')


class RestaurantCommentSerializer(ModelSerializer):
    user = UserCommentSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', 'created_at')


class TimeSerializer(ModelSerializer):
    class Meta:
        model = Time
        fields = ('morning_time', 'afternoon_time', 'evening_time')


class BookingSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Booking
        fields = ('id', 'date', 'morning', 'afternoon', 'evening', 'user', 'restaurant', 'status')

    def validate(self, attrs):

        def validate(self, attrs):
            restaurant = attrs.get('restaurant')
            if isinstance(restaurant, Restaurant):
                attrs['restaurant'] = restaurant.pk
            return attrs

        if attrs.get('date') < timezone.now().date():
            raise ValidationError("You cannot book for a past date")

        morning = attrs.get('morning')
        afternoon = attrs.get('afternoon')
        evening = attrs.get('evening')
        restaurant = attrs.get('restaurant')
        date = attrs.get('date')

        if morning and Booking.objects.filter(restaurant=restaurant, date=date, morning=True).exists():
            raise ValidationError("The morning time slot is already booked")

        if afternoon and Booking.objects.filter(restaurant=restaurant, date=date, afternoon=True).exists():
            raise ValidationError("The afternoon time slot is already booked")

        if evening and Booking.objects.filter(restaurant=restaurant, date=date, evening=True).exists():
            raise ValidationError("The evening time slot is already booked")

        if not morning and not afternoon and not evening:
            raise ValidationError("Please select at least one time slot")

        return attrs


class BookingListSerializer(ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = Booking
        fields = ('id', 'date', 'morning', 'afternoon', 'evening', 'user', 'restaurant', 'status')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        image_urls = [request.build_absolute_uri(image.image.url) for image in
                      instance.restaurant.restaurant_images.all()]

        selected_times = []
        if representation.get('morning'):
            selected_times.append('morning')
        if representation.get('afternoon'):
            selected_times.append('afternoon')
        if representation.get('evening'):
            selected_times.append('evening')

        if request and request.user.is_admin:
            return {
                'id': representation.get('id'),
                'restaurant_name': instance.restaurant.name,
                'date': representation.get('date'),
                'time': selected_times,
                'customer': {
                    'full_name': instance.user.full_name,
                    'image': request.build_absolute_uri(instance.user.image.url) if instance.user.image else None,
                    'phone': instance.user.phone,
                },
                'status': representation.get('status'),
            }
        else:
            return {
                'id': representation.get('id'),
                'restaurant': {
                    'id': instance.restaurant.id,
                    'name': instance.restaurant.name,
                    'images': image_urls,
                    'phone': instance.restaurant.phone,
                },
                'date': representation.get('date'),
                'time': selected_times,
                'status': representation.get('status'),
            }


class BookingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'status')

    def validate(self, attrs):
        status = attrs.get('status')
        if status not in ['pending', 'approved', 'rejected']:
            raise ValidationError("Invalid status")
        return attrs

    @staticmethod
    def send_booking_status_email(instance):
        user = instance.user
        subject = f"Booking {instance.status.capitalize()}"
        html_content = render_to_string('booking_email_template.html',
                                        {'status': instance.status, 'user': user, 'booking_status': instance.status})
        text_content = strip_tags(html_content)
        from_email = f"ADORE TEAM <{settings.EMAIL_HOST_USER}>"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.send_booking_status_email(instance)
        return instance


class TimeSerializerModelSerializer(ModelSerializer):
    class Meta:
        model = Time
        fields = ['morning_time', 'afternoon_time', 'evening_time', 'restaurant']






