import folium
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]

DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_image_url(request, pokemon_instance):
    if not pokemon_instance.image:
        return DEFAULT_IMAGE_URL
    return request.build_absolute_uri(pokemon_instance.image.url)


def add_pokemon(map_object, latitude, longitude, image_url):
    icon = None
    if image_url:
        icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))

    popup_message = image_url if image_url else "No Image"

    folium.Marker(
        location=[latitude, longitude],
        icon=icon,
        popup=popup_message
    ).add_to(map_object)


def show_all_pokemons(request):
    now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities_page = []
    for pokemon_entity in pokemon_entities:
        image_url = get_image_url(request, pokemon_entity.pokemon)
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            image_url
        )
        pokemon_entities_page.append({
            'pokemon_id': pokemon_entity.pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon_entity.pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemon_entities_page,
    })


def get_evolution_data(pokemon_instance, request):
    if not pokemon_instance:
        return None

    return {
        'title': pokemon_instance.title,
        'img': get_image_url(request, pokemon_instance),
        'pokemon_id': pokemon_instance.id,
    }


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    previous_evolution_entity = get_evolution_data(pokemon.previous_evolutions.first(), request)

    next_evolution_entity = get_evolution_data(pokemon.next_evolution, request)

    pokemon_data = {
        'title': pokemon.title,
        'title_en': pokemon.title_en,
        'title_ja': pokemon.title_ja,
        'img_url': get_image_url(request, pokemon),
        'description': pokemon.description,
        'evolved_from': previous_evolution_entity,
        'evolves_to': next_evolution_entity,
    }

    return render(request, 'pokemon.html', context={
        'pokemon': pokemon_data,
    })
