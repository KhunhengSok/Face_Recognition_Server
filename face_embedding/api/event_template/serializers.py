from rest_framework import serializers
from django.contrib.auth.models import User

from face_embedding.models import Event, EventTemplate
from face_embedding.api.organization.serializers import OrganizationSerializer
from face_embedding.api.account.serializers import UserSerializer


class EventTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTemplate
        fields = '__all__'

    def to_representation(self, instance):
        data = super(EventTemplateSerializer, self).to_representation(instance)
        data['organization_id'] = data['organization']
        del data['organization']
        return data

    def validate_name(self, value):
        name = self.initial_data['name']
        try:
            templates = EventTemplate.objects.filter(organization=self.initial_data['organization']).all()
        except EventTemplate.DoesNotExist:
            pass

        for template in templates.iterator():
            if template.name == name:
                if self.instance and self.instance.id == template.id:
                    continue
                else:
                    raise serializers.ValidationError(
                        {'name': 'Template with this name is already exist in the organization'})
        return value


