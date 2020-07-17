from django.contrib.auth.models import User

from face_embedding.models import Organization, Employee


def validate_email(email):
    errors = {}
    if email == '':
        errors = {
            'email': 'email is needed '
        }
        return False, errors
    try:
        user = User.objects.get(email=email)
        if user:
            errors = {
                'email': 'The message is already in use',
            }
            return False, errors
        else:
            return True, errors
    except User.DoesNotExist:
        return True, errors


def validate_username(username, organization_name):
    """
        No employee with same first and last name in the organization
    """
    errors = {}
    if username == '':
        errors = {
            'username': 'username is needed'
        }
    # if organization_name == '':
    #     errors = {
    #         'organization_name': 'organization_name is needed'
    #     }

    # if it's invalid
    if len(errors) != 0:
        return False, errors
    else:
        return True, errors

    # try:
    #     organization = Organization.objects.get(name=organization_name)
    #     employee = employee.objects.get(organization=organization, name=name)
    #     if employee:
    #         errors = {
    #             'name': 'The name is already exist in your organization.'
    #         }
    #         return False, errors
    #     else:
    #         return True, errors
    # except Organization.DoesNotExist:
    #     return True, errors
