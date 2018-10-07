from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe

class WarningMessage(models.Model):
    describe = models.CharField(max_length=300)
    face = models.ImageField(upload_to='img')
    create_date_time = models.DateTimeField(auto_now_add=True)

