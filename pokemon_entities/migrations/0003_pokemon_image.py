# Generated by Django 5.1.2 on 2024-10-18 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_alter_pokemon_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pokemon_images/'),
        ),
    ]
