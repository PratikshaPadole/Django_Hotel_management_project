# Generated by Django 4.1.6 on 2023-03-14 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_hotels_rooms_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='room',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='hotel',
        ),
        migrations.DeleteModel(
            name='Hotels',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Rooms',
        ),
    ]
