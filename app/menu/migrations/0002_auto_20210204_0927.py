# Generated by Django 3.1.3 on 2021-02-04 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name': 'Danie', 'verbose_name_plural': 'Dania'},
        ),
        migrations.AlterField(
            model_name='dish',
            name='created',
            field=models.DateTimeField(blank=True, verbose_name='Utworzono'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='updated',
            field=models.DateTimeField(blank=True, verbose_name='Zaktualizowano'),
        ),
    ]
