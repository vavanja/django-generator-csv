# Generated by Django 4.1.7 on 2023-03-14 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_delete_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='')),
                ('status', models.CharField(default='Processing', max_length=50, null=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('download_link', models.CharField(max_length=250, null=True)),
                ('schema_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.dataschema')),
                ('user_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
