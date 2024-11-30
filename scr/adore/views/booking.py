from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scr.adore.models.booking import Comment, Booking, Time
from scr.adore.serializers.booking import CommentSerializer, BookingSerializer, BookingUpdateSerializer, \
    BookingListSerializer, TimeSerializerModelSerializer


class CommentCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class BookingCreateAPIView(CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_admin:
            return Booking.objects.filter(restaurant__user=self.request.user)
        else:
            return Booking.objects.filter(user=self.request.user)


class BookingUpdate(UpdateAPIView):
    """
    ## pending -> approved -> rejected
    """

    queryset = Booking.objects.all()
    serializer_class = BookingUpdateSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put']

    def get_queryset(self):
        if self.request.user.is_admin:
            return Booking.objects.filter(restaurant__user=self.request.user)
        else:
            return Booking.objects.filter(user=self.request.user)


class TimeListAPIView(ListAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializerModelSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Format: YYYY-MM-DD"),
            openapi.Parameter('restaurant_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Restaurant ID")
        ]
    )
    def get(self, request, *args, **kwargs):
        restaurant_id = self.request.query_params.get('restaurant_id')
        date = self.request.query_params.get('date')

        if not date or not restaurant_id:
            return Response([])

        date = datetime.strptime(date, '%Y-%m-%d').date()
        if date < datetime.now().date():
            return Response("Invalid date. Date cannot be in the past.", status=400)

        self.queryset = self.queryset.filter(restaurant__id=restaurant_id)

        response = super().get(request, *args, **kwargs)

        for item in response.data:
            morning_time = item.get('morning_time')
            afternoon_time = item.get('afternoon_time')
            evening_time = item.get('evening_time')

            if morning_time:
                is_morning_busy = Booking.objects.filter(restaurant__id=restaurant_id, date=date,
                                                         morning=True).exists()
                item['morning_time'] = not is_morning_busy
            if afternoon_time:
                is_afternoon_busy = Booking.objects.filter(restaurant__id=restaurant_id, date=date,
                                                           afternoon=True).exists()
                item['afternoon_time'] = not is_afternoon_busy
            if evening_time:
                is_evening_busy = Booking.objects.filter(restaurant__id=restaurant_id, date=date,
                                                         evening=True).exists()
                item['evening_time'] = not is_evening_busy

        return Response(response.data)




