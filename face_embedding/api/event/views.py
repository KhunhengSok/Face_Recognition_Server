from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from face_embedding.api.employee.serializers import EmployeeSerializer

from .serializers import EventSerializer
from face_embedding.models import Organization,  Event
from face_embedding.api.employee.views import validate_organization_admin


def get_event(id, not_found_handling=False):
    event = None
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        if not_found_handling:
            return Response({
                'message': 'Event not found'
            }, status=HTTP_404_NOT_FOUND)
    return event


@api_view(('Get',))
def show(request, id):
    event = Event.objects.get(pk=id)
    serializer = EventSerializer(event)
    return Response(serializer.data, HTTP_200_OK)


@api_view(('Post',))
@permission_classes([IsAuthenticated])
def create(request):
    data = request.data
    data['created_by'] = request.user.id
    org = Organization.objects.get(name=data['organization'])
    data['organization'] = org.id
    data['attendees'] = []
    if validate_organization_admin(request, org):
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(serializer.data, HTTP_201_CREATED)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(('Post', 'Put',))
@permission_classes([IsAuthenticated])
def update(request, id):
    event = get_event(id, True)
    data = request.data
    try:
        org = Organization.objects.get(name=data['organization'])
        data['organization'] = org.id
    except KeyError:
        pass
    serializer = EventSerializer(instance=event, data=request.data, partial=True)

    if serializer.is_valid():
        event = serializer.save()
        return Response(serializer.data, HTTP_200_OK)
    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(("Delete",))
@permission_classes([IsAuthenticated])
def delete(request, id):
    event = get_event(id, True)
    org = Organization.objects.get(pk=event.organization.id)
    if validate_organization_admin(request, org):
        num = event.delete()
        return Response({
            'message': f'event {id} deleted'
        }, status=HTTP_200_OK)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(('Get',))
def show_attendees(request, id):
    event = get_event(id, True)
    attendees = event.attendees.all()
    serializer = EmployeeSerializer(attendees, many=True)
    return Response(serializer.data, status=HTTP_200_OK)