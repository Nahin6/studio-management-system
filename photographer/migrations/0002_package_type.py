# Generated by Django 4.0.2 on 2024-05-17 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='type',
            field=models.TextField(blank=True),
        ),
    ]