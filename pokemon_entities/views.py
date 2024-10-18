import folium
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from .models import Pokemon
from .models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]

DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(map_object, latitude, longitude, image_url):
    if image_url:
        icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))
        folium.Marker(
            location=[latitude, longitude],
            icon=icon,
            popup=image_url
        ).add_to(map_object)
    else:
        folium.Marker(
            location=[latitude, longitude],
            popup="No Image"
        ).add_to(map_object)


def show_all_pokemons(request):
    now = localtime()
    active_pokemons = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in active_pokemons:
        image_url = request.build_absolute_uri(pokemon.pokemon.image.url) if pokemon.pokemon.image else None
        add_pokemon(
            folium_map,
            pokemon.latitude,
            pokemon.longitude,
            image_url
        )

    pokemons_on_page = []
    for pokemon in active_pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.pokemon.image.url) if pokemon.pokemon.image else None,
            'title_ru': pokemon.pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    evolved_from = None
    if pokemon.evolved_from:
        evolved_from = {
            'title': pokemon.evolved_from.title,
            'img': request.build_absolute_uri(pokemon.evolved_from.image.url) if pokemon.evolved_from.image else None,
        }

    next_evolution = pokemon.evolutions.first()
    next_evolution_data = None
    if next_evolution:
        next_evolution_data = {
            'title': next_evolution.title,
            'level': 32,
        }

    pokemon_data = {
        'title': pokemon.title,
        'title_en': pokemon.title_en,
        'title_ja': pokemon.title_ja,
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
        'description': pokemon.description,
        'evolved_from': evolved_from,
        'next_evolution': next_evolution_data,
    }

    return render(request, 'pokemon.html', context={
        'pokemon': pokemon_data,
    })
