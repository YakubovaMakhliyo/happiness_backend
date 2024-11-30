from django.urls import path

from scr.adore.views.booking import *
from scr.adore.views.region import *
from scr.adore.views.restaurant import *

urlpatterns = [
    path("region", RegionListAPIView.as_view()),
    path("district", DistrictListAPIView.as_view()),
    path("mahalla", MahallaListAPIView.as_view()),

    path("service", ServiceListAPIView.as_view()),

    path("comment", CommentCreateAPIView.as_view()),
    path("search", RestaurantSearch.as_view()),

    path("restaurant", RestaurantCreateAPIView.as_view()),
    path("restaurant/image", RestaurantImageCreateAPIView.as_view()),
    path("restaurant/image/<int:pk>", RestaurantImageUpdateDestroyAPIView.as_view()),
    path("restaurant/my", MyRestaurantListAPIView.as_view()),
    path("restaurant/list", RestaurantListAPIView.as_view()),
    path("restaurant/detail/<int:pk>", RestaurantRetrieveAPIView.as_view()),
    path("restaurant/<int:pk>", RestaurantUpdateDestroyAPIView.as_view()),

    path("booking", BookingCreateAPIView.as_view()),
    path("booking/my", BookingListAPIView.as_view()),
    path("booking/<int:pk>", BookingUpdate.as_view()),
    path("booking/free", TimeListAPIView.as_view()),

]
