from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_ja = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    evolved_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='evolutions')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    objects = None
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    attack = models.IntegerField(default=10)
    defense = models.IntegerField(default=10)
    stamina = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.pokemon.title} at ({self.latitude}, {self.longitude})"
