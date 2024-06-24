from django.contrib import admin

from card.models import Card, MyCard


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'stock')
    search_fields = ('profile_rel.national_id', 'card_number')


@admin.register(MyCard)
class MyCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'cvv2', 'expiration_date')
    search_fields = ('card_number',)
