from django.contrib import admin
from  . import models

admin.site.register(models.User)
admin.site.register(models.Meeting)
admin.site.register(models.Umr)
admin.site.register(models.Message)
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Answer)
