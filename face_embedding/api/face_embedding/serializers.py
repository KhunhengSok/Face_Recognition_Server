from rest_framework import serializers
from django.contrib.auth.models import User

from face_embedding.models import Organization, FaceEmbedding


def format_face_embedding(array):
    return ', '.join(str(ele) for ele in array)


def get_face_embedding(representation_string):
    if representation_string != '':
        r = representation_string.split(', ')
        try:
            l = list(float(ele) for ele in r)
        except ValueError:
            l = []
        return l
    else:
        return []


class FaceEmbeddingSerializer(serializers.ModelSerializer):
    face_embedding = serializers.ListField()
    image_url = serializers.URLField()

    class Meta:
        model = FaceEmbedding
        fields = '__all__'
        extra_kwargs: {
            'image_url': {
                'write_only': True
            },
            'face_embedding': {
                'write_only': True
            },
            'owner': {
                'write_only': True
            }
        }

    def to_internal_value(self, data):
        rets = super(FaceEmbeddingSerializer, self).to_internal_value(data=data)
        embedding = data.get('face_embedding')
        if not (type(embedding[0]) == int or type(embedding[0]) == float):
            raise serializers.ValidationError({
                'face_embedding': 'face_embedding need to be float or integer'
            })
        rets['face_embedding'] = format_face_embedding(embedding)
        return rets