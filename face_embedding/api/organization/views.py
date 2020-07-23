from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from face_embedding.api.employee.serializers import EmployeeSerializer
from face_embedding.api.event.serializers import EventSerializer

from .serializers import OrganizationSerializer
from face_embedding.models import Organization, Employee


@api_view(('Get',))
def show(request, id):
    try:
        organization = Organization.objects.get(id=id)
    except Organization.DoesNotExist:
        return Response({
            'message': f'organization {id} is not found.',

        }, status=HTTP_404_NOT_FOUND)
    org_serializer = OrganizationSerializer(organization)

    return Response(data=org_serializer.data, status=HTTP_200_OK)


@api_view(('Post',))
@permission_classes([IsAuthenticated])
def create(request):
    data = request.data
    user = request.user
    data['created_by'] = user.id

    organization = OrganizationSerializer(data=data)
    if organization.is_valid():
        org = organization.save()
        serializer = EmployeeSerializer(data={
            'name': user.username,
            'email': user.email,
            'role': 'admin',
            'position':  'N/A',
            'department': 'N/A',
            'organization': org.id,
        })
        if serializer.is_valid():
            serializer.validated_data['organization'] = org
            serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)
        return JsonResponse(organization.data, status=HTTP_201_CREATED)
    else:
        return Response(organization.errors)


@api_view(('Post', 'Put'))
@permission_classes([IsAuthenticated])
def update(request, id):
    user = request.user
    try:
        org = Organization.objects.get(pk=id)
        serializer = OrganizationSerializer(instance=org, data=request.data,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    except Organization.DoesNotExist:
        return Response({
            'message': f'organization {id} not found'
        }, HTTP_400_BAD_REQUEST)


# url: api/organization/<id>/employees
@api_view(('Get',))
@permission_classes([IsAuthenticated])
def show_employees(request, id):
    try:
        org = Organization.objects.get(pk=id)
        employees = org.employee.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Organization.DoesNotExist:
        return Response({
            'message': f'organization {id} not found'
        }, HTTP_400_BAD_REQUEST)


# url: api/organization/<id>/events
@api_view(('Get',))
@permission_classes([IsAuthenticated])
def show_events(request, id):
    try:
        org = Organization.objects.get(pk=id)
    except  Organization.DoesNotExist:
        return Response({
            'message': f'organization {id} not found'
        }, HTTP_400_BAD_REQUEST)

    events = org.event
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, HTTP_200_OK)
