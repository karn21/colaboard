from django.contrib import admin

from .models import Board, BoardList, ListCard


admin.site.register(Board)
admin.site.register(BoardList)
admin.site.register(ListCard)
