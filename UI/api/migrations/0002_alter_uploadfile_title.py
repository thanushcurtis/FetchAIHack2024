# Generated by Django 5.0.1 on 2024-03-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]