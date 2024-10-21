from django.contrib import admin

from .models import Pokemon, PokemonEntity


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title', 'evolves')
    search_fields = ('title',)
    list_filter = ('evolves',)


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity)
