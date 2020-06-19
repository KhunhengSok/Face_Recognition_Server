from django.db import models
from picklefield.fields import PickledObjectField
from django_mysql.models import ListCharField
from django.utils import timezone

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
    

#Store image_url and face embedding from that url
#Many to one relationship with Person Model



# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    # image_url = models.TextField(null=True, editable=True)
    # face_embedding = models.TextField(null=True, editable=True,)

    created_at = models.DateTimeField(editable=False, null=True)
    update_at = models.DateTimeField(null=True)
    # face_embedding = PickledObjectField(null=True, default=None, editable=True)

    def save(self, *args, **kwargs):
        '''On save, update the updated_at field, and set the created_at when first save'''
        if not self.id:
            self.created_at = timezone.now()
        self.update_at = timezone.now()
        return super(Person,self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}. Created_at: {self.created_at}, updated_at: {self.update_at}"

class FaceEmbedding(models.Model):
    face_embedding = models.TextField( null=False, editable=True,)
    image_url = models.TextField(null=False,  editable=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="face")

    def __str__(self):
        return f"Username: {self.person.first_name} Url:{self.image_url}"