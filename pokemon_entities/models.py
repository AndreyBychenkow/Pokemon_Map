from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название (англ.)')
    title_ja = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название (яп.)')
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    evolved_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='evolutions', verbose_name='Эволюционирует из')
    evolves_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='previous_forms', verbose_name='Эволюционирует в')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Появился в')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Исчез в')
    level = models.IntegerField(default=1, verbose_name='Уровень')
    health = models.IntegerField(default=100, verbose_name='Здоровье')
    attack = models.IntegerField(default=10, verbose_name='Атака')
    defense = models.IntegerField(default=10, verbose_name='Защита')
    stamina = models.IntegerField(default=10, verbose_name='Выносливость')

    def __str__(self):
        return f"{self.pokemon.title} at ({self.latitude}, {self.longitude})"
