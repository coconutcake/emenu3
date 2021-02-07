# Generated by Django 3.1.3 on 2021-02-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nazwa')),
                ('description', models.TextField(verbose_name='Opis')),
                ('price', models.FloatField(verbose_name='Cena')),
                ('etc', models.DurationField(verbose_name='Czas oczekiwania')),
                ('created', models.DateTimeField(blank=True, null=True, verbose_name='Utworzono')),
                ('updated', models.DateTimeField(blank=True, null=True, verbose_name='Zaktualizowano')),
                ('is_vege', models.BooleanField(verbose_name='Danie wegańskie')),
            ],
            options={
                'verbose_name': 'Danie',
                'verbose_name_plural': 'Dania',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nazwa unikalna menu')),
                ('created', models.DateTimeField(blank=True, null=True, verbose_name='Utworzono')),
                ('updated', models.DateTimeField(blank=True, null=True, verbose_name='Zaktualizowano')),
                ('dish', models.ManyToManyField(to='menu.Dish', verbose_name='Danie')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menu',
            },
        ),
    ]
