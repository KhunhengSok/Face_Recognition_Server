from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .serializers import EmployeeSerializer
from face_embedding.models import Organization, Employee


# urls: /employee/<id>
@api_view(('Get',))
def show(request, id):
    try:
        employee = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, HTTP_200_OK)
    except Organization.DoesNotExist:
        return Response({
            'employee': {
                'employee': 'Employee does not exist'
            }
        }, HTTP_404_NOT_FOUND)
    return Response(None)


# urls: /employee/create
@api_view(('Post',))
@permission_classes([IsAuthenticated])
def create(request):
    data = request.data
    try:
        organization = Organization.objects.get(name=data['organization'])
        data['organization'] = organization.id
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.save()
            return Response(serializer.data, HTTP_201_CREATED)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    except Organization.DoesNotExist:
        raise serializers.ValidationError(
            {
                'organization': {
                    'organization': "Organization not found"
                }
            }
        )


# urls: /employee/<id>/update
@api_view(('Post',))
@permission_classes([IsAuthenticated])
def update(request, id):
    data = request.data
    organization = Organization.objects.get(name=data['organization'])
    data['organization'] = organization
    try:
        employee = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(employee, data=request.data)
        # serializer.update(employee, validated_data=request.data)

        # return Response(serializer.data, HTTP_200_OK)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    except Employee.DoesNotExist:
        return Response({
            'employee': {
                'employee' : 'Employee does not exist'
            }
        }, HTTP_404_NOT_FOUND)
    return Response(None)
