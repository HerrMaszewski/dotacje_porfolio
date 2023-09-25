# Generated by Django 4.2.5 on 2023-09-25 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dotacje', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('1', 'Fundacja'), ('2', 'Organizacja pozarządowa'), ('3', 'Lokalna zbiórka')], default='1', max_length=25),
        ),
    ]
