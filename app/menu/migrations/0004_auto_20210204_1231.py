# Generated by Django 3.1.3 on 2021-02-04 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20210204_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='created',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Utworzono'),
        ),
        migrations.AddField(
            model_name='menu',
            name='updated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Zaktualizowano'),
        ),
    ]