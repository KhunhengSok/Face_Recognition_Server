from collections import OrderedDict

from rest_framework import serializers
from face_embedding.models import Employee, Organization
from face_embedding.api.organization.serializers import OrganizationSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    # id = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'role', 'birth_of_date', 'position', 'department',
                  'organization', 'employed_date', 'created_at', 'updated_at', 'profile_url'
                  ]
        read_only_fields = ['organization']

    def validate_name(self, value):
        name = self.initial_data['name']
        try:
            employees = Employee.objects.filter(organization=self.initial_data['organization']).all()
        except Employee.DoesNotExist:
            pass
        for e_name in employees.iterator():
            if e_name.name == name:
                if self.instance and e_name.id != self.instance.id:
                    continue
                else:
                    raise serializers.ValidationError(
                        {'name': {'name': 'Employee with this name is already exist in the organization'}})
        return value

    def to_representation(self, instance):
        data = super(EmployeeSerializer, self).to_representation(instance)
        print('organization: ', data.keys())
        try:
            org = Organization.objects.get(pk=data['organization'])
            # del data['organization']
            data['organization'] = OrganizationSerializer(org).data
            return data
        except Organization.DoesNotExist:
            raise KeyError('not found')
        return data




