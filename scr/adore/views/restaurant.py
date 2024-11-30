from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scr.adore.models.booking import Time
from scr.adore.pagination import CustomPagination
from scr.adore.serializers.restaurant import *


class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    permission_classes = (IsAuthenticated,)


class RestaurantCreateAPIView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer
    permission_classes = (IsAuthenticated,)


class RestaurantImageCreateAPIView(CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = MultipleImageSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = MultipleImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantImageUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = RestaurantImageModelSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put', 'delete']


class RestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    pagination_class = CustomPagination


class MyRestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = MyRestaurantListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)


class RestaurantRetrieveAPIView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailModelSerializer


class RestaurantUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class RestaurantSearch(ListAPIView):
    serializer_class = RestaurantListSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('region_id', openapi.IN_QUERY, description="Region ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('district_id', openapi.IN_QUERY, description="District ID", type=openapi.TYPE_INTEGER),
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        region_id = self.request.query_params.get('region_id', None)
        district_id = self.request.query_params.get('district_id', None)

        if region_id is not None:
            queryset = queryset.filter(address__mahalla__district__region__id=region_id)

        if district_id is not None:
            queryset = queryset.filter(address__mahalla__district__id=district_id)

        return queryset
