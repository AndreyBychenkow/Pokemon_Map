from django.contrib import admin

from .models import Pokemon, PokemonEntity


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title', 'next_evolution')
    search_fields = ('title',)
    list_filter = ('next_evolution',)


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity)
