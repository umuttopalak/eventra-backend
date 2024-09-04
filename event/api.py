from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils import CustomErrorResponse, CustomSuccessResponse

from .models import Event
from .serializers import EventSerializer


class PublicEventAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            events = Event.objects.filter(is_active=True, is_deleted=False)
            serializer = EventSerializer(events, many=True)
            return CustomSuccessResponse(status_code=status.HTTP_200_OK, input_data=serializer.data)
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))


class EventAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return CustomSuccessResponse(status_code=status.HTTP_200_OK, input_data=serializer.data)
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))

    def post(self, request):
        try:
            request_data = request.data.copy()
            request_data['created_by'] = request.user.id

            serializer = EventSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return CustomSuccessResponse(input_data=serializer.data, status_code=status.HTTP_201_CREATED)
            return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST, msj=serializer.errors)
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))


class EventDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return CustomSuccessResponse(input_data=serializer.data, status_code=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Event not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))

    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomSuccessResponse(input_data=serializer.data, status_code=status.HTTP_200_OK)
            return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST, msj=serializer.errors)
        except Event.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Event not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))

    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return CustomSuccessResponse(status_code=status.HTTP_204_NO_CONTENT, msj="Event deleted successfully")
        except Event.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Event not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))


class JoinEventAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)

            if event.participants.count() >= event.max_participants:
                return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST, msj="Max participants limit reached.")

            if request.user in event.participants.all():
                return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST, msj="You have already joined this event.")

            event.participants.add(request.user)
            event.save()

            return CustomSuccessResponse(status_code=status.HTTP_200_OK, msj="Successfully joined the event.")
        except Event.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Event not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))


class LeaveEventAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)

            if request.user not in event.participants.all():
                return CustomErrorResponse(status_code=status.HTTP_400_BAD_REQUEST, msj="You are not a participant of this event.")

            event.participants.remove(request.user)
            event.save()

            return CustomSuccessResponse(status_code=status.HTTP_200_OK, msj="Successfully left the event.")
        except Event.DoesNotExist:
            return CustomErrorResponse(status_code=status.HTTP_404_NOT_FOUND, msj="Event not found")
        except Exception as e:
            return CustomErrorResponse(status_code=status.HTTP_502_BAD_GATEWAY, msj=str(e))
