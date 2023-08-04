from django.contrib import admin
<<<<<<< HEAD
from .models import *
# Register your models here.


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)
=======
from vote import models

admin.site.register(models.Poll)
admin.site.register(models.Choice)
admin.site.register(models.NonUserVote)
admin.site.register(models.UserVote)
admin.site.register(models.TempUser)
>>>>>>> 9a582c9e1128f8d07e4d79aa1a98a5100133c0dd
