# Generated by Django 5.2.1 on 2025-05-31 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-rating', 'created_at'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AddField(
            model_name='property',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('Apartment', 'Apartment'), ('House', 'House'), ('Studio', 'Studio'), ('Room', 'Room'), ('Loft', 'Loft'), ('Penthouse', 'Penthouse'), ('Bungalow', 'Bungalow'), ('Villa', 'Villa'), ('Tiny House', 'Tiny House'), ('Mobile Home', 'Mobile Home')], default='Apartment', max_length=40),
        ),
    ]
