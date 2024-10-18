# admin.py
from django.contrib import admin

from .models import Pokemon, PokemonEntity


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title', 'evolved_from')
    search_fields = ('title',)
    list_filter = ('evolved_from',)


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity)
