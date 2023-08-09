from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(UserVote)
admin.site.register(NonUserVote)
admin.site.register(Comment)