from django.contrib import admin

from card.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'stock')
    search_fields = ('profile_rel.national_id', 'card_number')
