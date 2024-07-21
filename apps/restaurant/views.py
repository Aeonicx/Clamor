from .models import Restaurant
from .serializers import RestaurantReadSerializer, RestaurantWriteSerializer
from django.http import Http404
from rest_framework.views import APIView
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.hours.serializers import BusinessHourSerializer, HolidayHourSerializer
from common.permissions import UserBasedPermission, IsLoggedInOrReadOnly
from common.pagination import MyLimitOffsetPagination
from apps.category.serializers import CategoryReadSerializer


class RestaurantProfile(APIView):
    """
    Get login user restaurant.
    """

    @swagger_auto_schema(operation_id="restaurant_read")
    def get(self, request, format=None):
        restaurants = request.user.restaurants.all()
        if restaurants.exists():
            restaurant = restaurants.last()
            serializer = RestaurantReadSerializer(restaurant)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404


class RestaurantList(APIView):
    """
    List all restaurants, or create a new restaurant.
    """

    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsLoggedInOrReadOnly]

    def get(self, request, format=None):
        queryset = Restaurant.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = RestaurantReadSerializer(page, many=True)

        next_link = paginator.get_next_link()
        previous_link = paginator.get_previous_link()
        count = paginator.count

        return Response(
            count=count,
            previous=previous_link,
            next=next_link,
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=RestaurantWriteSerializer)
    def post(self, request, format=None):
        serializer = RestaurantWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            restaurant = serializer.save(user=user, created_by=user)
            serializer = RestaurantReadSerializer(restaurant)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class RestaurantDetail(APIView):
    """
    Retrieve, update or delete a restaurant instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = Restaurant.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        serializer = RestaurantReadSerializer(restaurant)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=RestaurantWriteSerializer)
    def patch(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        serializer = RestaurantWriteSerializer(
            restaurant, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            restaurant = serializer.save(updated_by=request.user)
            serializer = RestaurantReadSerializer(restaurant)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class RestaurantBusinessHourList(APIView):
    """
    Retrieve business-hours of a restaurant.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = Restaurant.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        business_hours = restaurant.business_hours.all()
        serializer = BusinessHourSerializer(business_hours, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RestaurantHolidayHourList(APIView):
    """
    Retrieve holiday-hours of a restaurant.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = Restaurant.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)

        holiday_hours = restaurant.holiday_hours.all()
        serializer = HolidayHourSerializer(holiday_hours, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RestaurantCategoryList(APIView):
    """
    Retrieve categories of a restaurant.
    """

    permission_classes = []

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        categories = restaurant.categories.all()
        serializer = CategoryReadSerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
