from collections import OrderedDict

from rest_framework import serializers
from face_embedding.models import Employee, Organization, FaceEmbedding
from face_embedding.api.organization.serializers import OrganizationSerializer
from face_embedding.api.face_embedding.serializers import FaceEmbeddingSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    # faces = serializers.RelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'role', 'birth_of_date', 'position', 'department',
                  'organization',  'organization_id',  'employed_date', 'created_at', 'updated_at', 'profile_url',
                  ]
        extra_kwargs: {
            'organization': {
                'read_only': False
            }
        }
        # organization = serializers.PrimaryKeyRelatedField(many=False, read_only=False)

    def validate_name(self, value):
        name = self.initial_data['name']
        try:
            employees = Employee.objects.filter(organization=self.initial_data['organization']).all()
        except Employee.DoesNotExist:
            # print('can find the employee')
            pass
        for e_name in employees.iterator():
            if e_name.name == name :
                if self.instance and e_name.id == self.instance.id:
                    continue
                else:
                    raise serializers.ValidationError(
                        {'name': 'Employee with this name is already exist in the organization'})
        return value

    def to_representation(self, instance):
        data = super(EmployeeSerializer, self).to_representation(instance)

        try:
            org = Organization.objects.get(pk=data['organization'])
            del data['organization']
            # data['organization'] = OrganizationSerializer(org).data
            try:
                faces = FaceEmbedding.objects.filter(owner=instance.id).all()
                print(faces)
                # data['faces'] = FaceEmbeddingSerializer(faces, many=True).data
            except FaceEmbedding.DoesNotExist:
                data['faces'] = []
            return data
        except Organization.DoesNotExist:
            raise KeyError('not found')
        return data



