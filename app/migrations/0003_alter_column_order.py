# Generated by Django 4.1.7 on 2023-03-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_column_name_alter_column_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]