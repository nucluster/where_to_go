# Generated by Django 3.2.12 on 2022-03-05 18:00

from django.db import migrations, models
import places.models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=places.models.media_directory_path),
        ),
    ]
