from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework import serializers

from rest_framework.permissions import IsAuthenticated
from face_embedding.api.employee.serializers import EmployeeSerializer

from .serializers import EventSerializer, EmployeeEventSerializer
from face_embedding.models import Organization,  Event, Employee_Event
from face_embedding.api.employee.views import validate_organization_admin
# from face_embedding.serializers import get_face_embedding
from face_embedding.api.face_embedding.serializers import get_face_embedding
from scipy.spatial.distance import cosine
import datetime

MIN_DISTANCE = 0.38


def get_event(id, not_found_handling=False):
    event = None
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)



@api_view(('Get',))
def show(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)

    serializer = EventSerializer(instance=event)
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
            # data['created_by'] = request.user.id
            serializer.validated_data['created_by'] = request.user
            event = serializer.save()
            return Response(serializer.data, HTTP_201_CREATED)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "message": "unauthorized"
        }, status=HTTP_401_UNAUTHORIZED)


@api_view(('Post', 'Put',))
@permission_classes([IsAuthenticated])
def update(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)
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
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)
    org = Organization.objects.get(pk=event.organization.id)
    if validate_organization_admin(request, org):
        num = event.delete()
        return Response({
            'message': f'event {id} deleted'
        }, status=HTTP_200_OK)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(('Get',))
def show_all_attendees(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)
    attendees = event.attendees.all()

    EmployeeEventSerializer()
    serializer = EmployeeSerializer(attendees, many=True)
    return Response(serializer.data, status=HTTP_200_OK)



# url: api/event/<id>/absent
@api_view(('Get',))
def show_absent_attendees(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)
    organization = Organization.objects.get(pk=event.organization.id)
    all_attendees = event.attendees.all()
    employees = organization.employee.all()
    absence = []
    for employee in employees.iterator():
        if employee not in all_attendees:
            absence.append(employee)

    serializer = EmployeeSerializer(absence, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


# url: api/event/<id>/early
@api_view(('Get',))
def show_early_attendees(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)
    # organization = Organization.objects.get(pk=event.organization.id)
    all_attendees = Employee_Event.objects.filter(event=event).all()
    start_time = event.start_time
    early_attendees = []
    for attendee in all_attendees.iterator():
        if attendee.attend_time <= start_time:
            employee_event = Employee_Event.objects.get(event=event, employee=attendee.employee)
            early_attendees.append(employee_event)

    serializer = EmployeeEventSerializer(instance=early_attendees, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


# url: api/event/<id>/late
@api_view(('Get',))
def show_late_attendees(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)
    all_attendees = Employee_Event.objects.filter(event=event).all()
    start_time = event.start_time
    late_attendees = []
    for attendee in all_attendees.iterator():
        if attendee.attend_time > start_time:
            employee_event = Employee_Event.objects.get(event=event, employee=attendee.employee)
            late_attendees.append(employee_event)

    serializer = EmployeeEventSerializer(instance=late_attendees, many=True)
    return Response(serializer.data, status=HTTP_200_OK)



# url: api/event/<id>/join
'''
request : {
    "attend_time": ""
    "face_embedding": []

}
'''

@api_view(('Post',))
def join(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({
            'message': 'Event not found'
        }, status=HTTP_404_NOT_FOUND)

    target_embedding = request.data['face_embedding']
    print(target_embedding)
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

                print(distance)
                if distance < 0.01:
                # if True:
                    d = {
                        "verified": True,
                        "name": employee.name,
                        "distance": distance,
                        "image_url": face.image_url,
                        "created_at": face.created_at,
                    }
                    data = {
                        'employee': employee.id,
                        'event': event.id,
                        'attend_time': request.data['attend_time']
                    }
                    serializer = EmployeeEventSerializer(data=data)

                    if serializer.is_valid():
                        serializer.save()
                        return Response(data, status=HTTP_200_OK)
                    else:
                        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

    return Response({
        'message': "Face not match"
    }, status=HTTP_404_NOT_FOUND)
