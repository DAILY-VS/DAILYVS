from django.contrib import admin
from .models import *

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Comment)
admin.site.register(Poll_Result)


class UserVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'choice']

admin.site.register(UserVote, UserVoteAdmin)

    

class NonUserVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'choice']

admin.site.register(NonUserVote, NonUserVoteAdmin)