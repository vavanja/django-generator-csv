# Generated by Django 4.1.7 on 2023-03-13 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_filename_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='filename',
            name='schema_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.dataschema'),
        ),
        migrations.AlterField(
            model_name='filename',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='filename',
            name='file_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='filename',
            name='status',
            field=models.CharField(default='Processing', max_length=50, null=True),
        ),
    ]
