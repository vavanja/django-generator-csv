# Generated by Django 4.1.7 on 2023-03-09 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Column name'),
        ),
        migrations.AlterField(
            model_name='column',
            name='order',
            field=models.IntegerField(blank=True),
        ),
    ]
