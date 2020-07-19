from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, AnonymousUser

from .serializers import EmployeeSerializer
from face_embedding.models import Organization, Employee
from face_embedding.api.face_embedding.serializers import FaceEmbeddingSerializer

def validate_organization_admin(request, organization):
    user = request.user
    employees = organization.employee.filter(role='admin').all()

    if user == AnonymousUser:
        return False
    else:
        for employee in employees:
            # same name under same organization
            if employee.name == user.username:
                return True
        return False


def get_organization(organization_id):
    try:
        org = Organization.objects.get(pk=organization_id)
        return org
    except Organization.DoesNotExist:
        return None


# urls: /employee/<id>
@api_view(('Get',))
def show(request, id):
    try:
        employee = Employee.objects.get(pk=id)
        org = get_organization(employee.organization.id)
        is_admin = validate_organization_admin(request, org)
        print(is_admin)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, HTTP_200_OK)
    except Employee.DoesNotExist:
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
        data['organization_id'] = organization.id
        serializer = EmployeeSerializer(data=request.data)

        try:

            FaceEmbeddingSerializer()
        except KeyError:
            pass

        if serializer.is_valid():
            serializer.validated_data['organization'] = organization
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
@api_view(('Post', 'Put'))
@permission_classes([IsAuthenticated])
def update(request, id):
    data = request.data
    user = request.data
    try:
        organization = Organization.objects.get(name=data['organization'])
    except KeyError as e:
        return Response(e, HTTP_400_BAD_REQUEST)
    except Organization.DoesNotExist:
        return Response({
            'organization': {
                'organization': "organization not found"
            }

        })
    data['organization'] = organization

    try:
        employee = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(instance=employee, data=request.data, partial=True)
        # serializer.update(employee, validated_data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    except Employee.DoesNotExist:
        return Response({
            'employee': {
                'employee': 'Employee does not exist'
            }
        }, HTTP_404_NOT_FOUND)
    return Response(None)


# urls: api/emplyoee/<id>/delete
@api_view(("Delete",))
@permission_classes([IsAuthenticated])
def delete(request, id):
    employee = Employee.objects.get(pk=id)
    org = employee.organization
    if validate_organization_admin(request, org):
        employee.delete()
        return Response({
            'message': f'employee {id} deleted'
        }, HTTP_200_OK)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)