from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework import serializers

from rest_framework.permissions import IsAuthenticated

from .serializers import FaceEmbeddingSerializer
from face_embedding.models import Organization, Employee, FaceEmbedding
from .serializers import get_face_embedding
from scipy.spatial.distance import cosine

MIN_DISTANCE = 0.38


# urls: api/organization/<id>face-embedding/create
'''
{
    "owner": "khunheng",
    "face_embedding": [
        1,5,5
    ],
    "image_url": "https://www.facebook.com"
}
'''
@api_view(('Post',))
@permission_classes([IsAuthenticated])
def create(request, id):
    data = request.data
    try:
        # org = Organization.objects.get(pk=id)
        employee = Employee.objects.filter(name=data['owner']).filter(organization=id).get()
    except Employee.DoesNotExist:
        return Response({
            'employee': f'employee {data["owner"]} not found in organization_id {id}'
        }, HTTP_400_BAD_REQUEST)
    except Organization.DoesNotExist:
        return Response({
            'organization': f'organization {id} not found.'
        }, HTTP_400_BAD_REQUEST)

    data['owner'] = employee.id

    serializer = FaceEmbeddingSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['owner'] = employee
        face_embedding = serializer.save()

        return Response({
            'message': f'Face Embedding with id {face_embedding.id} created successfully '
        }, HTTP_200_OK)
    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


# urls: api/organization/<id>face-embedding/compare
@api_view(('Post',))
@permission_classes([IsAuthenticated])
def recognize(request, id):
    target_embedding = request.data['face_embedding']
    try:
        org = Organization.objects.get(pk=id)
        # get all employees in the organization
        employees = org.employee.all()
    except Organization.DoesNotExist:
        return Response({
            'organization': f'organization {id} not found.'
        }, HTTP_400_BAD_REQUEST)

    matched_faces = []
    for employee in employees.iterator():
        # get all face_embedding for current employee
        faces = employee.face.all()
        if len(faces) == 0:
            continue
        else:
            for face in faces:
                embedding_array = get_face_embedding(face.face_embedding)
                try:
                    distance = cosine(embedding_array, target_embedding)
                except ValueError or TypeError:
                    distance = float('inf')

                if distance < MIN_DISTANCE:
                    d = {
                        "verified": True,
                        "name": employee.name,
                        "distance": distance,
                        "image_url": face.image_url,
                        "created_at": face.created_at,
                    }
                    matched_faces.append(d)
                    break
    data = {
        'faces': matched_faces
    }

    return Response(data=data, status=HTTP_200_OK)
