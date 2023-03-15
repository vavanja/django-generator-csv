from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.contrib.auth.models import User
from django.urls import reverse


class User(AbstractUser):

    def __str__(self):
        return self.username


class DataSchema(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    modified = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_columns_children(self):
        return self.column_set.all()

    def get_absolute_url(self):
        return reverse('update_schema', args=[str(self.id)])
        # return f'/update/{self.id}/'


class Column(models.Model):
    DATA_TYPE_CHOICES = [
        ('Full name', 'Full name'),
        ('Job', 'Job'),
        ('Email', 'Email'),
        ('Phone number', 'Phone number'),
        ('Date', 'Date'),
    ]

    name = models.CharField('Column name', unique=True, max_length=100)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, blank=False, null=False)
    extra_args = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(blank=True, null=True)
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class FileName(models.Model):
    status = models.CharField(default='Processing', null=True, max_length=50)
    date_created = models.DateField(auto_now_add=True, null=True)
    download_link = models.CharField(null=True, max_length=250)
    schema_id = models.ForeignKey(DataSchema, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
