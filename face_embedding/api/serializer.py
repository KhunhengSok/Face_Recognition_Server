from rest_framework import serializers
from face_embedding.models import Person, get_face_embedding


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'image_url', ]
        # fields = ['first_name', 'last_name', 'image_url',  'face_embedding','created_at',  ]

    def to_representation(self, instance):
        output = super(PersonSerializer, self).to_representation(instance)
        output['face_embedding'] = get_face_embedding(output['face_embedding'])
        return output
