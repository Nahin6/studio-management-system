# Generated by Django 4.0.2 on 2024-05-19 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_hiringdetails_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hiringdetails',
            name='photographer_id',
            field=models.IntegerField(default=None),
        ),
    ]
