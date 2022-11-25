# Create your models here.
from django.db import models
## models.py
from django.conf import settings
# Add the import for GridFSStorage
# from djongo.storage import GridFSStorage
# # Define your GrifFSStorage instance
# grid_fs_storage = GridFSStorage(collection='myfiles')
import uuid
import os



class Document(models.Model):
    sno = models.AutoField(primary_key=True)
    docfile = models.FileField(upload_to='documents')
