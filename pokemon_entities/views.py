import folium
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

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
    pokemon_entity = get_object_or_404(PokemonEntity, id=pokemon_id)
    pokemon = pokemon_entity.pokemon

    folium_map = folium.Map(location=[pokemon_entity.latitude, pokemon_entity.longitude], zoom_start=12)

    add_pokemon(
        folium_map,
        pokemon_entity.latitude,
        pokemon_entity.longitude,
        request.build_absolute_uri(pokemon.image.url) if pokemon.image else None
    )

    pokemon_data = {
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_ja': pokemon.title_ja,
        'description': pokemon.description,
        'level': pokemon_entity.level,
        'health': pokemon_entity.health,
        'attack': pokemon_entity.attack,
        'defense': pokemon_entity.defense,
        'stamina': pokemon_entity.stamina,
        'appeared_at': pokemon_entity.appeared_at,
        'disappeared_at': pokemon_entity.disappeared_at,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data,
    })
