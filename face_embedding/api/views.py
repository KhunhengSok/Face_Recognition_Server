from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.parsers import JSONParser

from scipy.spatial.distance import cosine

from .serializer import PersonSerializer
from face_embedding.models import Person, FaceEmbedding,  format_face_embedding, get_face_embedding


MIN_DISTANCE = 0.38

# @api_view(('POST',))
# def create(request):
#     print('create attemp')
#     if request.method == "POST":
#         try:
#             first_name = request.data['first_name']
#             last_name = request.data['last_name']
#             #Todoss
#             image_url = request.data['image_url']
#             face_embedding = request.data['face_embedding']
#             embedding_str = format_face_embedding(face_embedding)
#             request.data['face_embedding']  =embedding_str

#         except KeyError:
#             data = {
#                 "message": "Key not found"
#             }
#             return Response(data=data, status=HTTP_400_BAD_REQUEST)
        
#         # pickle = PickledObjectField()
#         # print(face_embedding)
#         person = Person(first_name, last_name, image_url, face_embedding=embedding_str)
#         serializer = PersonSerializer(data=request.data )

#         if serializer.is_valid():
#             serializer.save()
#             data = {
#                 "serializer": serializer.data,
#                 "message":  "created successfully"
#             }
#             return Response(data=data, status=HTTP_201_CREATED)
           
#         else:
#             data = {
#                 "message": "Serializer is not valid."
#             }
#             return Response(data=data, status=HTTP_400_BAD_REQUEST)

# [
#     {
#         "face_embedding": "",
#         "url": ''
#     }
# ]

@api_view(('POST',))
def create(request):
    print('create attemp')
    if request.method == "POST":
        try:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            #Todoss
            image_url = request.data['image_url']
            face_embedding = request.data['face_embedding']
            embedding_str = format_face_embedding(face_embedding)
            request.data['face_embedding']  =embedding_str

        except KeyError:
            data = {
                "message": "Key not found"
            }
            return Response(data=data, status=HTTP_400_BAD_REQUEST)
        
        # pickle = PickledObjectField()
        # print(face_embedding)
        person = Person(first_name, last_name, image_url, face_embedding=embedding_str)
        serializer = PersonSerializer(data=request.data )

        if serializer.is_valid():
            serializer.save()
            data = {
                "serializer": serializer.data,
                "message":  "created successfully"
            }
            return Response(data=data, status=HTTP_201_CREATED)
           
        else:
            data = {
                "message": "Serializer is not valid."
            }
            return Response(data=data, status=HTTP_400_BAD_REQUEST)

@api_view( ('POST', ))
def update(request):
    pass

    
@api_view( ('POST',))
def compare(request):
    '''
        verified: True,
        distance: 0.0f,
        time: 0s,
        face_id: 
        person: 
        face_rectangle: {
            top,
            left,
            width,
            height
        }
        
    '''
    # source_face_embedding = Person.objects.values('face_embedding')
    person = Person.objects.all()

    #validate request data
    try:
        target_face_embedding = request.data['face_embedding']
    except KeyError as e: 
        data = {}
        if hasattr(e, 'message'):
            data["message"]: e.message
        else:
            data['message'] = f"Can not find key {e} "

        return Response(data=data,status=HTTP_400_BAD_REQUEST)
    
    if type(target_face_embedding) != list:
        data = {
            "message": "face_embedding need to be array of int or array of float"
        }
        return Response(data=data,status=HTTP_400_BAD_REQUEST)

    if type(target_face_embedding[0]) != int and type(target_face_embedding[0]) != float: 
        data = {
            "message": "face_embedding need to be array of int or array of float"
        }
        return Response(data=data, status=HTTP_400_BAD_REQUEST)

    #start processing    
    faces = []
    for p in person: 
        try:
            person_faces = FaceEmbedding.objects.filter(person=p)
        except FaceEmbedding.DoesNotExist:
            #that person doesn't have face_embedding save yet
            continue

        for face in person_faces:
            face_embed = face.face_embedding
            embed = get_face_embedding(face_embed)
            try:
                distance = cosine(embed, target_face_embedding)
            except  ValueError and TypeError:
                continue
            print(distance)
            if distance < MIN_DISTANCE:
                d = {
                    "verified": True,
                    "first_name": p.first_name,
                    "last_name": p.last_name,
                    "distance": distance,
                    "image_url": face.image_url,
                    "created_at": p.created_at,
                    'updated_at': p.update_at
                }
                faces.append(d)
                break
    
    data = {}
    data['faces'] = faces
   

    return Response(data=data, status=HTTP_200_OK)

