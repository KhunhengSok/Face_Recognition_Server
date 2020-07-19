from rest_framework import serializers
from django.contrib.auth.models import User

from face_embedding.models import Event, Organization
from face_embedding.api.organization.serializers import OrganizationSerializer
from face_embedding.api.account.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'created_by', 'organization', 'date', 'start_time', 'end_time', 'attendees']
        extra_kwargs: {
            'attendees': {
                'required': False
            },

        }

    def to_representation(self, instance):
        data = super(EventSerializer, self).to_representation(instance)
        org = Organization.objects.get(pk=data['organization'] )
        user = User.objects.get(pk=data['created_by'])
        data['organization_id'] = data['organization']
        del data['organization']

        # data['organization'] = OrganizationSerializer(org).data
        data['created_by'] = UserSerializer(user).data
        return data
