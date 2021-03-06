from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# from rest_framework.authentication import authenticate

from face_embedding.models import User, Organization
from .serializers import UserSerializer
from face_embedding.api.organization.serializers import OrganizationSerializer
from .Authentication import MyTokenAuthentication
from .utils import validate_email, validate_username


# urls: localhost:8000/account/register
@api_view(('POST',))
@permission_classes([])
@authentication_classes([])
def register(request):
    data = {}

    userSerializer = UserSerializer(data=request.data)

    if userSerializer.is_valid():
        user = userSerializer.save()
        token = Token.objects.create(user=user)
        data = {
            'response': 'Successfully register new user',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'token': token.key
            }
        }

        return Response(data=data, status=HTTP_201_CREATED)
    else:
        data['error'] = userSerializer.errors
        return Response(data, status=HTTP_400_BAD_REQUEST)


# urls localhost:8000/account/login
@api_view(('Get',))
@permission_classes([IsAuthenticated])
def user(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=request.user)
    user = User.objects.get(username=request.user)
    data = {
        'id':       user.id,
        'username': user.username,
        'email':    user.email,
        'token':    token.key
    }
    return Response(data, status=HTTP_200_OK)


# urls localhost:8000/account/login
@api_view(('Post', 'Get',))
@permission_classes([])
def login(request):
    if request.method == "POST":
        user = authenticate(username=request.data['username'], password=request.data['password'])
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response({'user': "user not found"}, status=HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)


        data = {
            'id':       user.id,
            'username': user.username,
            'email':    user.email,
            'token':    token.key
        }
        return Response(data, status=HTTP_200_OK)
    elif request.method == 'GET':
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=request.user)
        user = User.objects.get(username=request.user)
        data = {
            'id':       user.id,
            'username': user.username,
            'email':    user.email,
            'token':    token.key
        }
        return Response(data, status=HTTP_200_OK)


# urls /account/<id>
@api_view(('Get',))
@permission_classes([])
def show(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data, HTTP_200_OK)


# urls /account/<id>organizations
@api_view(('Get',))
@permission_classes([IsAuthenticated])
def show_organizations(request, id):
    orgs = Organization.objects.filter(created_by=id).all()
    org_serializer = OrganizationSerializer(orgs, many=True)
    # print(org_serializer.is_valid(True))
    return Response(org_serializer.data, HTTP_200_OK)


# urls /account/<id>/update
# @api_view(('Put',))
# @permission_classes([IsAuthenticated])
# def update(request, id):
#     try:
#         User.objects.get(pk=id)
#     except User.DoesNotExist:
#         return Response(HTTP_404_NOT_FOUND)
#
#     serializer = UserSerializer(instance=user, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer, HTTP_200_OK)
#     else:
#         return Response(serializer.errors, HTTP_400_BAD_REQUEST)