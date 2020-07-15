from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .serializers import UserSerializer
from .Authentication import MyTokenAuthentication
from .utils import validate_email, validate_username


# urls: localhost:8000/account/signup
@api_view(('POST',))
@permission_classes([])
@authentication_classes([])
def register(request):
    data = {}

    # email = request.data.get('email', '')
    # is_valid, errors = validate_email(email)
    # if not is_valid:
    #     data['email'] = errors['email']
    #
    # username = request.data.get('username', '')
    # organization_name = request.data.get('organization_name', '')
    # is_valid, errors = validate_username(username, organization_name)
    # if not is_valid:
    #     for key in errors.keys():
    #         data[key] = errors[key]

    # if len(data) != 0:
    #     return Response(data=data, status=HTTP_400_BAD_REQUEST)
    # else:
    userSerializer = UserSerializer(data=request.data)

    if userSerializer.is_valid():
        user = userSerializer.save()
        data['response'] = 'Successfully register new user'
        data['email'] = user.email
        data['username'] = user.username
        token = Token.objects.create(user=user)
        data['token'] = token.key
        return Response(data=data, status=HTTP_201_CREATED)
    else:
        data['error'] = userSerializer.errors
        return Response(data, status=HTTP_400_BAD_REQUEST)


# urls localhost:8000/account/login
@api_view(('Post',))
@permission_classes([IsAuthenticated])
def login(request):
    print(request.user)
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=request.user)
    user = User.objects.get(username=request.user)
    data = {
        'username': user.username,
        'email':    user.email,
        'token':    token.key
    }
    return Response(data, status=HTTP_200_OK)


