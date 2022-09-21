from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class faculty_details(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)
    idno = models.IntegerField(null=False, unique=True, blank=False)
    timetable = ArrayField(ArrayField(models.CharField(max_length=30, null=False, blank=False), size=9))
