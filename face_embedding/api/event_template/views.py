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

from .serializers import EventTemplateSerializer
from face_embedding.models import Organization,  Event, EventTemplate
from face_embedding.api.employee.views import validate_organization_admin


# def get_event(id, not_found_handling=False):
#     event = None
#     try:
#         event = Event.objects.get(pk=id)
#     except Event.DoesNotExist:
#         if not_found_handling:
#             return Response({
#                 'message': 'Event not found'
#             }, status=HTTP_404_NOT_FOUND)
#     return event


@api_view(('Get',))
def show(request, id):
    try:
        template = EventTemplate.objects.get(pk=id)
    except EventTemplate.DoesNotExist:
        return Response({
            'message': f"Template {id} not found"
        }, HTTP_400_BAD_REQUEST)

    serializer = EventTemplateSerializer(template)
    return Response(serializer.data, HTTP_200_OK)

@api_view(('Post',))
@permission_classes([IsAuthenticated])
def create(request):
    user = request.user
    data = request.data
    data['created_by'] = user.id
    try:
        org = Organization.objects.get(name=data['organization'])
        data['organization'] = org.id
    except KeyError:
        pass
    except Organization.DoesNotExist:
        return Response({
            'message': f"Organization {data['organization']} not found"
        }, HTTP_400_BAD_REQUEST)

    serializer = EventTemplateSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.validated_data['organization'] = org
        except KeyError:
            pass
        event_template = serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(('Post', 'Put',))
@permission_classes([IsAuthenticated])
def update(request, id):
    try:
        template = EventTemplate.objects.get(pk=id)
        serializer = EventTemplateSerializer(instance=template, data=request.data, partial=True)
        if serializer.is_valid():
            template = serializer.save()
            return Response(serializer.data, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    except EventTemplate.DoesNotExist:
        return Response({
            'message': f"Template {id} not found"
        }, HTTP_400_BAD_REQUEST)


@api_view(("Delete",))
@permission_classes([IsAuthenticated])
def delete(request, id):
    try:
        template = EventTemplate.objects.get(pk=id)

    except EventTemplate.DoesNotExist:
        return Response({
            'message': f"Template {id} not found"
        }, HTTP_400_BAD_REQUEST)

    org = template.organization
    if validate_organization_admin(request, org):
        org.delete()
        return Response({
            'message': f'employee {id} deleted'
        }, HTTP_200_OK)
    else:
        return Response(HTTP_401_UNAUTHORIZED)

