# Generated by Django 4.2.9 on 2024-01-18 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название места')),
                ('description_short', models.TextField(verbose_name='Краткое описание')),
                ('description_long', models.TextField(verbose_name='Полное описание')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('latitude', models.FloatField(verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='places/', verbose_name='Файл')),
                ('url', models.URLField(blank=True, verbose_name='Внешний URL')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Позиция')),
                ('image_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Порядковый номер фото')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
                'ordering': ['order'],
            },
        ),
    ]
