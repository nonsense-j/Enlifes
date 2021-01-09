from django.contrib import admin
from .models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ['cid', 'cdisry', 'create_time', 'title', 'detail']
    ordering = ['create_time']
    list_filter = ['cdisry']

    list_per_page = 5
