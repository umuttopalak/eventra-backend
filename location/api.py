from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView, status

from utils import CustomErrorResponse, CustomSuccessResponse

from .models import Location
from .serializers import LocationSerializer


class LocationAPI(APIView):
    def get(self, request):
        try:
            locations = Location.objects.all()
            serializer = LocationSerializer(locations, many=True)
            return CustomSuccessResponse(status_code=status.HTTP_200_OK, input_data=serializer.data)
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))

    def post(self, request):
        try:
            request_data = request.data
            serializer = LocationSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return CustomSuccessResponse(input_data=serializer.data, status_code=status.HTTP_200_OK)
            return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY)


class LocationDetailAPI(APIView):
    def get(self, request, pk):
        location = Location.objects.get(pk=pk)
        if location is None:
            serializer = LocationSerializer(location)
            return CustomSuccessResponse(input_data=serializer.data, status_code=status.HTTP_200_OK)
        return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomSuccessResponse(input_data=serializer.data, status_code=status.HTTP_200_OK)
            return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST, msj=serializer.errors)
        except Location.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Location not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))

    def delete(self, request, pk):
        try:
            location = Location.objects.get(pk=pk)
            location.is_deleted = True
            location.save()
            return CustomSuccessResponse(status_code=status.HTTP_204_NO_CONTENT, msj="Location deleted successfully")
        except Location.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Location not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))
