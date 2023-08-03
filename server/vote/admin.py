from django.contrib import admin
from vote import models

admin.site.register(models.Poll)
admin.site.register(models.Choice)
admin.site.register(models.NonUserVote)
admin.site.register(models.UserVote)
admin.site.register(models.TempUser)