from rest_framework import serializers
from django.contrib.auth.models import User
from face_embedding.models import Organization


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        user = User.objects.get(pk =value)
        data = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
        return data


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'created_by', 'created_at']
        extra_kwargs = {
            'created_by': {
                'required': True,
            }

        }

    def to_representation(self, instance):
        data = super(OrganizationSerializer, self).to_representation(instance)
        data['name'] = instance.name.title()
        try:
            user = User.objects.get(username=instance.created_by)
            user_serializer = UserSerializer(user.id)
            data['created_by'] = user_serializer.data
            return data
        except User.DoesNotExist:
            pass
