# Generated by Django 4.0.2 on 2024-05-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0003_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='type',
            field=models.IntegerField(blank=True),
        ),
    ]
