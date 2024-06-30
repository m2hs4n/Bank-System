from django.contrib import admin

from token_check.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'stock')
